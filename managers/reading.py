from sqlalchemy import select

from managers.base import BaseDataManager
from models.reading import ReadingModel
from schemas.reading import ProgressSchema


class ReadingDataManager(BaseDataManager):
    def get_reading(self, reading_id):
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id)

        reading = self.get_one(stmt, ProgressSchema)

        print('')
