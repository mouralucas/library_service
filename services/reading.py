import datetime

from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from managers.item import ItemDataManager
from managers.reading import ReadingDataManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse, CreateProgressResponse, CreateReadingResponse
from services.base import BaseService


class ReadingService(BaseService):

    async def create_reading(self, reading: CreateReadingRequest) -> CreateReadingResponse:
        """ TODO:
                1: Check if the item already have a reading
                2: If a previous reading exist:
                    2.1: Check if the reading is active, if so cannot create a new one, if not, create a new one
                    2.2: Count the number of readings and set a variable with the value
                    2.3: A new reading cannot start before the previous finish, check the dates
        """
        param = {
            'item_id': reading.item_id
        }
        previous_readings = await ReadingDataManager(self.session).get_readings(params=param)
        last_reading = previous_readings[0] if previous_readings else None

        # Cannot start a new reading with another still active
        if last_reading and last_reading.active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe uma leitura ativa para este item')

        # The new reading cannot start before the last one finishes
        if last_reading and last_reading.finish_date and last_reading.finish_date > reading.start_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Uma leitura não pode ser iniciada antes de finalizar a anterior')

        new_reading = ReadingModel(
            item_id=reading.item_id,
            number=len(previous_readings) + 1,
            start_date=reading.start_at,
            finish_date=reading.finish_at,
            status_id='reading'  # maybe a param? If a param, update status column in Item model?
        )
        #
        new_reading = await ReadingDataManager(self.session).create_reading(reading=new_reading)
        response = CreateReadingResponse(
            status_code=status.HTTP_201_CREATED,
            reading=new_reading
        )
        return response

    async def get_reading(self, params: GetReadingRequest) -> GetReadingResponse:
        # TODO: add param checking if user want to include available progress in reading
        stmt = select(ReadingModel).options(joinedload(ReadingModel.progress)).where(ReadingModel.item_id == params.item_id)

        item = await ItemDataManager(self.session).get_item_by_id(item_id=params.item_id)
        reading = await ReadingDataManager(self.session).get_all(stmt, schema=ReadingSchema, unique_result=True)

        response = GetReadingResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            item_title=item.title,
            quantity=len(reading) if reading else 0,
            readings=reading
        )

        return response

    async def create_progress(self, progress: CreateProgressRequest) -> CreateProgressResponse:
        # TODO: Rules:
        #   One entry must not save a page and/or percentage less than the last entry
        #   If more than one entry is set in same day, the entry is update, not create another line (only one entry per day)
        reading = await ReadingDataManager(self.session).get_reading_by_id(progress.reading_id)
        last_progress = await ReadingDataManager(self.session).get_latest_progress(progress.reading_id)

        item_pages = reading.item.pages

        new_progress_entry = ReadingProgressModel(
            reading_id=reading.id,
            date=datetime.datetime.now().date(),
            rate=progress.rate,
            comment=progress.comment
        )

        if progress.page is not None:
            perc = ((progress.page / item_pages) * 100) if item_pages else 0

            new_progress_entry.page = progress.page
            new_progress_entry.percentage = perc

        if progress.percentage is not None:
            page = (progress.percentage / 100) * item_pages if item_pages else 0
            new_progress_entry.page = int(page)
            new_progress_entry.percentage = progress.percentage

        new_entry = await ReadingDataManager(self.session).create_progress(progress=new_progress_entry)

        response = CreateProgressResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            currentReadingProgress=new_entry
        )

        return response

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        progress = await ReadingDataManager(self.session).get_progress(reading_id=params.reading_id)

        response = GetProgressResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            quantity=len(progress),
            readingProgress=progress
        )

        return response
