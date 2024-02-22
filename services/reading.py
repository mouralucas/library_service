import datetime

from fastapi import status
from sqlalchemy import select

from managers.reading import ReadingDataManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse, CreateProgressResponse
from services.base import BaseService


class ReadingService(BaseService):

    def create_reading(self, reading: CreateReadingRequest):
        new_reading = ReadingModel(
            item_id=reading.item_id,
            number=1,
            start_at=reading.start_at,
            end_at=reading.finish_at,
            is_dropped=reading.is_dropped
        )

        new_reading = ReadingDataManager(self.session).create_reading(reading=new_reading)

        return new_reading

    async def get_reading(self, params: GetReadingRequest) -> GetReadingResponse:
        # TODO: add param checking if user want to include available progress in reading
        stmt = select(ReadingModel).where(ReadingModel.item_id == params.item_id)

        reading = await ReadingDataManager(self.session).get_all(stmt, ReadingSchema)

        response = GetReadingResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            quantity=len(reading),
            readings=reading
        )

        return response

    async def create_progress(self, progress: CreateProgressRequest) -> CreateProgressResponse:
        # TODO: Rules:
        #   The return must contain the reading description with the item name
        #   One entry must not save a page and/or percentage less than the last entry
        #   If more than one entry is set in same day, the entry is update, not create another line (only one entry per day)
        reading = await ReadingDataManager(self.session).get_reading_by_id(progress.reading_id)
        # TODO: Fetch last entry to validate date and current page/percentage

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
