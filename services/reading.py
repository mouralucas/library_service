from models.reading import ReadingModel
from schemas.reading import CreateReading
from services.base import BaseService
from managers.reading import ReadingDataManager


class ReadingService(BaseService):

    def create_reading(self, reading: CreateReading):
        new_reading = ReadingModel(
            item_id=reading.item_id,
            number=1,
            start_at=reading.start_at,
            end_at=reading.finish_at,
            is_dropped=reading.is_dropped
        )

        new_reading = ReadingDataManager(self.session).add_one(new_reading)

        return new_reading
