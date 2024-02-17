from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from managers.base import BaseDataManager
from models.reading import ReadingModel
from schemas.reading import ProgressSchema, ReadingSchema


class ReadingDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_reading(self, reading_id):
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id)

        reading = await self.get_one(stmt, ReadingSchema)

        print('')
