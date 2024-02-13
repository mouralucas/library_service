from sqlalchemy import select

from models.reading import ReadingModel
from schemas.reading import CreateReadingRequest, GetRedingResponse
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

    async def get_reading(self):
        stmt = select(ReadingModel).where(ReadingModel.id == '06f26836-cf1d-472e-add5-ab573cf7a018')

        reading = await ReadingDataManager(self.session).get_all(stmt, GetRedingResponse)

        return reading
