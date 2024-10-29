from datetime import datetime

from fastapi import status, HTTPException
from rolf_common.models import SQLModel
from rolf_common.schemas.auth import RequiredUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from managers.item import ItemManager
from managers.reading import ReadingDataManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema, ProgressSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse, CreateProgressResponse, CreateReadingResponse, GetActiveReadingsResponse
from services.base import BaseService


class ReadingService(BaseService):

    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()
        self.reading_manager = ReadingDataManager(session=self.session, user=self.user)

    async def create_reading(self, reading: CreateReadingRequest) -> CreateReadingResponse:
        param = {
            'item_id': reading.item_id
        }
        previous_readings = await self.reading_manager.get_readings(params=param)
        last_reading = previous_readings[0] if previous_readings else None

        # Cannot start a new reading with another still active
        if last_reading and last_reading.active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe uma leitura ativa para este item')

        # The new reading cannot start before the last one finishes
        if last_reading and last_reading.finish_date and last_reading.finish_date > reading.start_date:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Uma leitura não pode ser iniciada antes de finalizar a anterior')

        new_reading = ReadingModel(**reading.model_dump(exclude={'is_dropped'}))
        new_reading.number = len(previous_readings) + 1 if previous_readings else 1
        new_reading.owner_id = self.user['user_id']

        new_reading.status_id = 'read' if reading.finish_date else 'reading'
        new_reading.active = False if reading.finish_date else True

        new_reading = await self.reading_manager.create_reading(reading=new_reading)
        response = CreateReadingResponse(
            status_code=status.HTTP_201_CREATED,
            reading=ReadingSchema.model_validate(new_reading).transform()
        )
        return response

    async def get_reading(self, params: GetReadingRequest) -> GetReadingResponse:
        # TODO: put stmt logic in manager in existing get_readings
        stmt = select(ReadingModel).where(ReadingModel.owner_id == self.user['user_id'])

        if params.reading_id:
            stmt = stmt.where(ReadingModel.id == params.reading_id)

        if params.item_id:
            stmt = stmt.where(ReadingModel.item_id == params.item_id)

        if params.get_progress:
            progress_alias = aliased(ReadingProgressModel)
            stmt = stmt.options(joinedload(ReadingModel.progress.of_type(progress_alias))).order_by(progress_alias.date.desc())

        stmt = stmt.order_by(ReadingModel.start_date)

        readings = await self.reading_manager.get_all(stmt, unique_result=True, raise_exception=True)

        item = readings[0]['ReadingModel'].item if readings else None

        response = GetReadingResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            item_title=item.title,
            quantity=len(readings) if readings else 0,
            readings=[ReadingSchema.model_validate(reading['ReadingModel']) for reading in readings] if readings else []
        )

        return response

    async def get_active_readings(self) -> GetActiveReadingsResponse:
        # TODO: stmt should be in manager
        stmt = select(ReadingModel).where(ReadingModel.active == True,
                                          ReadingModel.owner_id == self.user['user_id'])

        readings = await self.reading_manager.get_all(stmt)

        response = GetActiveReadingsResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(readings) if readings else 0,
            readings=[ReadingSchema.model_validate(reading['ReadingModel']).transform() for reading in readings] if readings else []
        )

        return response

    async def create_progress(self, progress: CreateProgressRequest) -> CreateProgressResponse:

        reading = await self.reading_manager.get_reading_by_id(progress.reading_id, get_item=True)
        if not reading:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Reading not found')

        last_progress = await self.reading_manager.get_latest_progress(progress.reading_id)

        item = reading.item
        item_pages = item.pages

        # Current page/percentage can not be greater than last progress entry
        if ((last_progress and last_progress.page and progress.page and progress.page <= last_progress.page) or
                (last_progress and last_progress.percentage and progress.percentage and progress.percentage <= last_progress.percentage)):
            raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail='The current page/percentage could not be less than the last registered page')

        # Current page could not be greater then item pages
        if (item_pages and progress.page) and (progress.page > item_pages):
            raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail='Current page cannot be greater than the total pages of the item')

        # Only one entry per day is allowed
        if last_progress and last_progress.date == datetime.now().date():
            progress_updated = await self.reading_manager.update_progress(self.__set_values(progress_entry=last_progress, item_pages=item_pages,
                                                                                            current_page=progress.page, percentage=progress.percentage), {'page': progress.page})
            new_entry = progress_updated
        else:
            new_progress_entry = ReadingProgressModel(**progress.model_dump())
            new_progress_entry.item_id = reading.item_id
            new_entry = await self.reading_manager.create_progress(progress=self.__set_values(progress_entry=new_progress_entry, item_pages=item_pages,
                                                                                              current_page=progress.page, percentage=progress.percentage))

        # Update reading as read if pages == item.pages or percentage is 100%
        if ((item_pages and progress.page and item_pages == progress.page)
                or (progress.percentage and progress.percentage == 100)
                or (new_entry.percentage == 100)):
            await self.session.refresh(reading)
            await self.reading_manager.update_reading(reading=reading, fields={'active': False, 'status_id': 'read'})

        await self.session.refresh(item)
        await self.session.refresh(new_entry)

        response = CreateProgressResponse(
            success=True,
            item=item,
            progress=ProgressSchema.model_validate(new_entry)
        ).transform()

        return response

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        progress = await self.reading_manager.get_progress(reading_id=params.reading_id)
        # TODO: get from item, if none progress the item is None also, or maybe get from reading
        item = progress[0]['ReadingProgressModel'].item if progress else None

        response = GetProgressResponse(
            quantity=len(progress) if progress else 0,
            item=item,
            progress=[ProgressSchema.model_validate(i['ReadingProgressModel']) for i in progress] if progress else []
        ).transform()

        return response

    def __set_values(self, progress_entry: ReadingProgressModel, item_pages: int, current_page: int, percentage: int) -> SQLModel:
        if current_page is not None and current_page != 0:
            perc = ((current_page / item_pages) * 100) if item_pages else 0

            progress_entry.page = current_page
            progress_entry.percentage = perc

        if percentage is not None and percentage != 0:
            current_page = (percentage / 100) * item_pages if item_pages else 0
            progress_entry.page = int(current_page)
            progress_entry.percentage = percentage

        return progress_entry
