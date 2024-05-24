import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models.base import SQLModel
from models.reading import ReadingModel, ReadingProgressModel


class ReadingDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_reading(self, reading: ReadingModel) -> SQLModel:
        new_reading = await self.add_one(reading)

        return new_reading

    async def get_reading_by_id(self, reading_id) -> SQLModel:
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id)

        reading: SQLModel = await self.get_only_one(stmt)

        return reading

    async def get_readings(self, params: dict):
        stmt = select(ReadingModel)

        for key, value in params.items():
            stmt = stmt.where(getattr(ReadingModel, key) == value)

        stmt = stmt.order_by(ReadingModel.start_date.desc())

        readings = await self.get_all(stmt)

        return readings

    async def create_progress(self, progress: ReadingProgressModel) -> SQLModel:
        new_progress = await self.add_one(progress)

        return new_progress

    async def update_progress(self, progress: ReadingProgressModel, fields: dict[str, Any]) -> SQLModel:
        fields['edited_at'] = datetime.datetime.utcnow()
        stmt = (
            update(ReadingProgressModel)
            .where(ReadingProgressModel.id == progress.id)
            .values(**fields)
        )

        progress = await self.update_one(sql_statement=stmt, model=progress)

        return progress

    async def get_progress(self, reading_id):
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id)

        progress_list = await self.get_all(stmt)

        return progress_list

    async def get_latest_progress(self, reading_id) -> ReadingProgressModel | None:
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id).order_by(ReadingProgressModel.date.desc())

        latest_progress = await self.get_first(stmt)

        return latest_progress
