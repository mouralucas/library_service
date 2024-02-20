from sqlalchemy import select

from managers.reading import ReadingDataManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse
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

        new_reading = ReadingDataManager(self.session).add_one(new_reading)

        return new_reading

    async def get_reading(self, params: GetReadingRequest) -> GetReadingResponse:
        stmt = select(ReadingModel).where(ReadingModel.item_id == params.item_id)

        reading = await ReadingDataManager(self.session).get_all(stmt, ReadingSchema)

        response = GetReadingResponse(
            success=True,
            status_code=200,
            quantity=len(reading),
            readings=reading
        )

        return response

    async def create_progress(self, progress: CreateProgressRequest):
        # TODO: Rules:
        #   The return must contain the reading description with the item name
        #   One entry must not save a page and/or percentage less than the last entry
        #   If more than one entry is set in same day, the entry is update, not create another line (only one entry per day)
        reading = await ReadingDataManager(self.session).get_reading(progress.reading_id)

        new_entry = ReadingProgressModel(**progress.model_dump())
        print('')

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        progress = await ReadingDataManager(self.session).get_progress(reading_id=params.reading_id)

        response = GetProgressResponse(
            success=True,
            status_code=200,
            quantity=len(progress),
            readingProgress=progress
        )

        return response
