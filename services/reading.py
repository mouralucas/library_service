from typing import Type

from sqlalchemy import select

from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema, ProgressSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse
from services.base import BaseService
from managers.reading import ReadingDataManager


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
        reading = ReadingDataManager(self.session).get_reading(progress.reading_id)

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == params.reading_id)

        progress = await ReadingDataManager(self.session).get_all(stmt, ProgressSchema)

        response = GetProgressResponse(
            success=True,
            status_code=200,
            quantity=len(progress),
            readingProgress=progress
        )

        return response
