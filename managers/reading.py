from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from managers.base import BaseDataManager
from models.base import SQLModel
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ProgressSchema, ReadingSchema


class ReadingDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_reading(self, reading_id):
        # TODO: create a param to chose if return is transformed or not (if that makes sense)
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id)

        reading: ReadingSchema | None = await self.get_one(stmt, ReadingSchema, raise_exception=True)

        return reading.transform()

    async def create_progress(self, progress: ReadingProgressModel) -> SQLModel:
        new_progress = await self.add_one(progress)

        return new_progress

    async def get_progress(self, reading_id):
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id)

        progress_list = self.get_all(stmt, ProgressSchema)

        return progress_list
