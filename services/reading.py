from typing import Any
import uuid
from datetime import datetime

from fastapi import HTTPException, status
from rolf_common.backend.logger import get_logger
from rolf_common.models import SQLModel
from rolf_common.schemas.auth import RequiredUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from managers.reading import ReadingManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.item import ItemSchema
from schemas.reading import ProgressSchema, ReadingSchema, ReadingStats
from schemas.request.reading import (
    CreateProgressRequestV2,
    CreateReadingRequest,
    GetProgressRequest,
    GetReadingRequest,
    GetReadingStatsRequest,
)
from schemas.response.reading import (
    CreateProgressResponse,
    CreateReadingResponse,
    CreateReadingResponseV2,
    GetActiveReadingsResponse,
    GetProgressResponse,
    GetReadingsResponse,
    GetReadingStatsResponse,
)
from services.base import BaseService


class ReadingService(BaseService):

    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()
        self.reading_manager = ReadingManager(session=self.session, user=self.user)

    async def create_reading(
        self, reading: CreateReadingRequest
    ) -> CreateReadingResponseV2:
        previous_readings = await self.reading_manager.get_readings(
            item_id=reading.item_id
        )
        last_reading = previous_readings[0] if previous_readings else None

        # Cannot start a new reading with another still active
        if last_reading and last_reading.active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma leitura ativa para este item",
            )

        # The new reading cannot start before the last one finishes
        if (
            last_reading
            and last_reading.finish_date
            and last_reading.finish_date > reading.start_date
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma leitura não pode ser iniciada \
                    antes de finalizar a anterior",
            )

        new_reading = ReadingModel(**reading.model_dump(exclude={"is_dropped"}))
        new_reading.number = len(previous_readings) + 1 if previous_readings else 1
        new_reading.owner_id = self.user["user_id"]

        new_reading.status_id = "read" if reading.finish_date else "reading"
        new_reading.active = False if reading.finish_date else True

        new_reading = await self.reading_manager.create_reading(reading=new_reading)
        
        response = CreateReadingResponseV2(
            created=True,
            reading_id=new_reading.id
        )
        return response

    async def get_readings(
        self,
        item_id: int | None = None,
        reading_id: uuid.UUID | None = None,
        get_progress: bool = False,
    ) -> dict[str, Any]:
        readings = await self.reading_manager.get_readings(
            item_id=item_id, reading_id=reading_id, get_progress=get_progress
        )
        
        response = {
            "quantity": len(readings) if readings else 0,
            "readings": readings,
        }

        return response

    async def get_reading_by_id(self, reading_id: uuid.UUID) -> GetReadingsResponse:
        reading = await self.reading_manager.get_reading_by_id(reading_id=reading_id)
        if not reading:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found"
            )

        response = GetReadingsResponse(
            quantity=1 if reading else 0,
            readings=[ReadingSchema.model_validate(reading)],
        )

        return response

    async def get_active_readings(self) -> GetActiveReadingsResponse:
        active_readings = await self.reading_manager.get_active_readings()
        
        response = GetActiveReadingsResponse(
            quantity=len(active_readings) if active_readings else 0,
            readings=(
                [
                    ReadingSchema.model_validate(reading)
                    for reading in active_readings
                ]
                if active_readings
                else []
            ),
        )

        return response

    async def create_progress_v2(self, progress: CreateProgressRequestV2):
        page = progress.value if progress.progress_type == "page" else None
        percentage = progress.value if progress.progress_type == "percentage" else None

        # TODO: add raise_exception param or kwarg for it
        reading = await self.reading_manager.get_reading_by_id(
            progress.reading_id, get_item=True
        )
        if not reading:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Reading not found")

        last_progress = await self.reading_manager.get_latest_progress(
            progress.reading_id
        )

        item = reading.item
        item_pages = item.pages

        # The new entry can not be older than the last progress entry
        if last_progress and last_progress.progress_date > progress.progress_date:
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="The new progress entry date can not be\
                    older than the last registered progress entry",
            )

        # Current page/percentage can not be greater than last progress entry
        if (
            last_progress and last_progress.page and page and page <= last_progress.page
        ) or (
            last_progress
            and last_progress.percentage
            and percentage
            and percentage <= last_progress.percentage
        ):
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="The current page/percentage could not \
                            be less than the last registered page",
            )

        # The Current page should not be greater than item pages
        if (item_pages and page) and (page > item_pages):
            error_txt = f"Current page ({page}) cannot be greater than the\
                total pages of the item ({item.pages})"
            get_logger().error(error_txt)
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail=error_txt
            )

        # Only one entry per day is allowed
        if last_progress and last_progress.progress_date == datetime.now().date():
            seted_progress = self.__set_values(
                progress_entry=last_progress,
                item_pages=item_pages,
                current_page=page,
                percentage=percentage,
            )
            progress_updated = await self.reading_manager.update_progress(
                seted_progress, {"page": seted_progress.page}
            )
            progress_updated.rate = progress.rate
            progress_updated.comment = progress.comment
            new_entry = progress_updated
        else:
            new_progress_entry = ReadingProgressModel(
                **progress.model_dump(exclude={"progress_type", "value"})
            )
            new_progress_entry.item_id = reading.item_id
            new_entry = await self.reading_manager.create_progress(
                progress=self.__set_values(
                    progress_entry=new_progress_entry,
                    item_pages=item_pages,
                    current_page=page,
                    percentage=percentage,
                )
            )

        # Update reading as read if pages == item.pages or percentage is 100%
        if (
            (item_pages and page and item_pages == page)
            or (percentage and percentage == 100)
            or (new_entry.percentage == 100)
        ):
            await self.session.refresh(reading)
            await self.reading_manager.update_reading(
                reading=reading,
                fields={
                    "active": False,
                    "status_id": "read",
                    "finish_date": datetime.today(),
                },
            )

        await self.session.refresh(item)
        await self.session.refresh(new_entry)

        # response = CreateProgressResponse(
        #     item=ItemSchema.model_validate(item),
        #     progress=ProgressSchema.model_validate(new_entry),
        #     # These fields are populated automatically after model validation
        #     item_title=None,
        #     pages_read=None,
        # )
        
        response = {
            "created": True,
            "item_title": new_entry.item.title,
            "reading_progress_id": new_entry.id
        }

        return response

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        reading = await self.reading_manager.get_reading_by_id(
            reading_id=params.reading_id
        )
        if not reading:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found"
            )

        progress: list[ReadingProgressModel] | None = (
            await self.reading_manager.get_progress(reading_id=params.reading_id)
        )

        item = reading.item

        response = GetProgressResponse(
            quantity=len(progress) if progress else 0,
            item=item,
            progress=(
                [ProgressSchema.model_validate(i) for i in progress] if progress else []
            ),
        )

        return response

    async def get_reading_stats(
        self, params: GetReadingStatsRequest
    ) -> GetReadingStatsResponse:
        item_readings = await self.reading_manager.get_readings(item_id=params.item_id)

        # Get information about the last reading
        readings_count = len(item_readings) if item_readings else 0
        last_reading = item_readings[0] if item_readings else None
        last_reading_date = last_reading.start_date if last_reading else None

        # Get information about the current reading
        current_reading = await self.reading_manager.get_item_active_reading(
            item_id=params.item_id
        )
        is_currently_reading = True if current_reading else False
        current_reading_id = current_reading.id if current_reading else None
        current_reading_progress = (
            await self.reading_manager.get_latest_progress(
                reading_id=current_reading.id
            )
            if current_reading
            else None
        )
        current_page = (
            current_reading_progress.page if current_reading_progress else None
        )
        current_percentage = (
            current_reading_progress.percentage if current_reading_progress else None
        )

        response = GetReadingStatsResponse(
            stats=ReadingStats(
                readings_count=readings_count,
                last_reading_date=last_reading_date,
                is_currently_reading=is_currently_reading,
                current_reading_id=current_reading_id,
                current_page=current_page,
                current_percentage=current_percentage,
                last_readings=(
                    [ReadingSchema.model_validate(reading) for reading in item_readings]
                    if item_readings
                    else []
                ),
            )
        )

        return response

    @staticmethod
    def __set_values(
        progress_entry: ReadingProgressModel,
        item_pages: int,
        current_page: int | None,
        percentage: int | None,
    ) -> SQLModel:
        if current_page is not None and current_page != 0:
            perc = ((current_page / item_pages) * 100) if item_pages else 0

            progress_entry.page = current_page
            progress_entry.percentage = perc

        if percentage is not None and percentage != 0:
            current_page = int((percentage / 100) * item_pages) if item_pages else 0
            progress_entry.page = int(current_page)
            progress_entry.percentage = percentage

        return progress_entry
