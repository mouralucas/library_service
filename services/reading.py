import uuid
from datetime import date, datetime
from typing import Any

from fastapi import HTTPException, status
from rolf_common.backend.logger import get_logger
from rolf_common.models import SQLModel
from rolf_common.schemas.auth import RequiredUser
from sqlalchemy.ext.asyncio import AsyncSession

from managers.item import ItemManager
from managers.reading import ReadingManager
from models.reading import ReadingModel, ReadingProgressModel, ReadingQueueModel
from schemas.reading import ReadingSchema
from schemas.request.reading import (
    CreateProgressRequestV2,
    CreateReadingGoalRequest,
    CreateReadingRequest,
    GetProgressRequest,
    GetReadingStatsRequest,
    UpdateReadingStatusRequest,
)
from schemas.response.reading import (
    GetReadingsResponse,
)
from services.base import BaseService


class ReadingService(BaseService):

    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()
        self.reading_manager = ReadingManager(session=self.session, user=self.user)

    async def create_reading(self, reading: CreateReadingRequest) -> dict[str, Any]:
        # Check if the item have a reading in progress
        active_reading = await self.reading_manager.get_item_active_reading(
            item_id=reading.item_id
        )
        if active_reading is not None:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Já existe uma leitura iniciada para esse item!",
            )

        last_readigns = await self.reading_manager.get_item_last_readings(
            item_id=reading.item_id
        )
        previous_completed_reading = last_readigns[0] if last_readigns else None

        # The new reading cannot start before the last one finishes
        # TODO: chek what happens when try to start a new reading with last reading
        #   without finish date, maybe we need to check only the last completed reading
        if (
            previous_completed_reading
            and previous_completed_reading["finish_date"]
            and previous_completed_reading["finish_date"] > reading.start_date
        ):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Uma leitura não pode ser iniciada \
                    antes de finalizar a anterior",
            )

        new_reading = ReadingModel(**reading.model_dump(exclude={"is_dropped"}))
        new_reading.number = (
            len(last_readigns) + 1
            if previous_completed_reading and last_readigns
            else 1
        )
        new_reading.owner_id = self.user["user_id"]

        new_reading.status_id = "read" if reading.finish_date else "reading"
        new_reading.active = False if reading.finish_date else True

        new_reading = await self.reading_manager.create_reading(reading=new_reading)

        # check if the item is in queue, if not, add to queue
        is_item_in_queue = await self.reading_manager.get_active_goal_by_item_id(
            item_id=reading.item_id
        )
        if not is_item_in_queue:
            new_goal = ReadingQueueModel(
                owner_id=self.user["user_id"],
                item_id=reading.item_id,
                year=reading.start_date.year,
            )
            await self.reading_manager.add_reading_queue(goal=new_goal)

        response = {
            "created": True,
            "reading_id": new_reading.id,
            "item_title": new_reading.item.title,
        }
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

    async def get_active_readings(self) -> dict[str, Any]:
        active_readings = await self.reading_manager.get_all_active_readings()

        response = {
            "quantity": len(active_readings) if active_readings else 0,
            "readings": active_readings if active_readings else [],
        }

        return response

    async def create_progress_v2(self, progress: CreateProgressRequestV2):
        # Set values for page and percentage based on the progress type
        page = progress.value if progress.progress_type == "page" else None
        percentage = progress.value if progress.progress_type == "percentage" else None

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
        if last_progress and last_progress.progress_date == date.today():
            seted_progress = self._set_values(
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
                progress=self._set_values(
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
            await self._finish_reading(reading_id=reading.id)

        await self.session.refresh(item)
        await self.session.refresh(new_entry)

        response = {
            "created": True,
            "item_title": new_entry.item.title,
            "reading_progress_id": new_entry.id,
        }

        return response

    async def get_progress(self, params: GetProgressRequest) -> dict[str, Any]:
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

        response = {
            "quantity": len(progress) if progress else 0,
            "item_title": item.title,
            "pages_read": self._get_progess_pages_read(progress=progress, item=item),
            "progress": progress,
        }

        return response

    # Goals
    async def create_goal(self, goal: CreateReadingGoalRequest) -> dict[str, Any]:
        current_goal = await self.reading_manager.get_active_goal_by_item_id(
            item_id=goal.item_id
        )
        if current_goal:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Já existe uma meta ativa para esse item!",
            )

        new_goal = ReadingQueueModel(**goal.model_dump())
        new_goal.owner_id = self.user["user_id"]

        new_goal = await self.reading_manager.add_reading_queue(goal=new_goal)

        response = {
            "created": True,
            "reading_goal_id": new_goal.id,
        }

        return response

    async def get_reading_stats(self, params: GetReadingStatsRequest) -> dict[str, Any]:
        item_readings = await self.reading_manager.get_readings(item_id=params.item_id)

        # Get information about the last reading
        readings_count = len(item_readings) if item_readings else 0
        last_reading = item_readings[0] if item_readings else None
        last_reading_date = last_reading["start_date"] if last_reading else None

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

        response = {
            "stats": {
                "readings_count": readings_count,
                "last_reading_date": last_reading_date,
                "is_currently_reading": is_currently_reading,
                "current_reading_id": current_reading_id,
                "current_page": current_page,
                "current_percentage": current_percentage,
                "last_readings": (
                    [ReadingSchema.model_validate(reading) for reading in item_readings]
                    if item_readings
                    else []
                ),
            }
        }

        return response

    async def get_reading_goals(self, year: int | None) -> dict[str, Any]:
        item_manager = ItemManager(session=self.session)

        goals = await self.reading_manager.get_reading_queue(year=year)
        goal_items_ids = [goal["item_id"] for goal in goals] if goals else None

        if goals:
            goal_items = await item_manager.get_detailed_items(id_list=goal_items_ids)
            items_map = await item_manager.get_items_indexed(goal_items)

            for goal in goals:
                goal["item"] = items_map.get(goal["item_id"])

        response = {
            "goals": goals if goals else [],
        }

        return response

    async def update_reading_status(
        self, params: UpdateReadingStatusRequest
    ) -> dict[str, Any]:
        reading = None
        if params.reading_id:
            reading = await self.reading_manager.get_reading_by_id(
                reading_id=params.reading_id
            )
        elif params.item_id:
            reading = await self.reading_manager.get_item_active_reading(
                item_id=params.item_id
            )

        if not reading:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found"
            )

        new_status = params.new_status

        # If the new status is "completed",
        #   set the finish date as today and active as false
        if new_status == "completed":
            await self._finish_reading(reading_id=reading.id)
        else:
            # If the new status is "reading",
            #   set the finish date as null and active as true
            # If the new status is "dropped",
            #   set the finish date as today and active as false
            fields = {
                "active": True if new_status == "reading" else False,
                "finish_date": None if new_status == "reading" else datetime.today(),
                "status_id": new_status,
            }
            await self.reading_manager.update_reading(reading=reading, fields=fields)

        response = {
            "updatedStatus": new_status,
            "itemTitle": reading.item.title,
        }

        return response

    @staticmethod
    def _get_progess_pages_read(progress, item):
        pages_read = ""
        if progress and progress[0].page and item.pages:
            pages_read = f"{progress[0].page}/{item.pages} - {progress[0].percentage}%"
        return pages_read

    async def _finish_reading(self, reading_id: uuid.UUID):
        reading = await self.reading_manager.get_reading_by_id(reading_id=reading_id)

        if not reading:
            raise  # TODO

        item = reading.item
        goal = await self.reading_manager.get_active_goal_by_item_id(item_id=item.id)

        # update reading
        await self.reading_manager.update_reading(
            reading=reading,
            fields={
                "active": False,
                "status_id": "read",
                "finish_date": datetime.today(),
            },
        )

        # If a goal exist for the item in current year, update the goal to achieved
        if goal:
            await self.reading_manager.update_goal(
                goal=goal, fields={"achieved": True, "date_achieved": datetime.now()}
            )

        return True

    @staticmethod
    def _set_values(
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
