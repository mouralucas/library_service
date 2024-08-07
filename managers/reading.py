from typing import Any

from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.reading import ReadingModel, ReadingProgressModel


class ReadingDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession, user: dict[str, Any] = None):
        super().__init__(session=session)
        self.user = user

    async def create_reading(self, reading: ReadingModel) -> SQLModel:
        new_reading = await self.add_one(reading)

        return new_reading

    async def update_reading(self, reading: SQLModel, fields: dict[str, Any]) -> SQLModel:
        stmt = (update(ReadingModel)
                .where(ReadingModel.id == reading.id)
                .values(**fields))

        reading = await self.update_one(sql_statement=stmt, sql_model=reading)

        return reading

    async def get_reading_by_id(self, reading_id, get_item: bool = False) -> SQLModel | None:
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id,
                                          ReadingModel.owner_id == self.user['user_id'])

        if get_item:
            stmt = stmt.options(joinedload(ReadingModel.item))

        reading: SQLModel = await self.get_only_one(stmt)

        return reading

    async def get_readings(self, params: dict) -> list[SQLModel] | None:
        # Only the owner can get the readings
        # Maybe in future this can be a param, to get reading for someone the user want
        stmt = select(ReadingModel).where(ReadingModel.owner_id == self.user['user_id'])

        for key, value in params.items():
            stmt = stmt.where(getattr(ReadingModel, key) == value)

        stmt = stmt.order_by(ReadingModel.start_date.desc())

        readings = await self.get_all(stmt)

        return readings

    async def get_item_active_reading(self, item_id: int) -> SQLModel | None:
        stmt = select(ReadingModel).where(ReadingModel.item_id == item_id, ReadingModel.active == 1)
        reading: SQLModel = await self.get_only_one(stmt)

        return reading

    # Progress Methods
    async def create_progress(self, progress: SQLModel) -> SQLModel:
        new_progress = await self.add_one(progress)

        return new_progress

    async def update_progress(self, progress: SQLModel, fields: dict[str, Any]) -> SQLModel:
        stmt = (
            update(ReadingProgressModel)
            .where(ReadingProgressModel.id == progress.id)
            .values(**fields)
        )

        progress = await self.update_one(sql_statement=stmt, sql_model=progress)

        return progress

    async def get_progress(self, reading_id):
        stmt = (select(ReadingProgressModel)
                .where(ReadingProgressModel.reading_id == reading_id)
                .order_by(ReadingProgressModel.date.desc()))

        progress_list = await self.get_all(stmt)

        return progress_list

    async def get_latest_progress(self, reading_id) -> ReadingProgressModel | None:
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id).order_by(ReadingProgressModel.date.desc())

        latest_progress = await self.get_first(stmt)

        return latest_progress
