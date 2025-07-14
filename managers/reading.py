from typing import Any, cast

from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.reading import ReadingModel, ReadingProgressModel


class ReadingManager(BaseDataManager):
    def __init__(self, session: AsyncSession, user: dict[str, Any] = None):
        super().__init__(session=session)
        self.user = user

    async def create_reading(self, reading: ReadingModel) -> ReadingModel:
        new_reading: SQLModel = await self.add_one(reading)

        return cast(ReadingModel, new_reading)

    async def update_reading(self, reading: SQLModel, fields: dict[str, Any]) -> ReadingModel:
        query = (update(ReadingModel)
                 .where(ReadingModel.id == reading.id)
                 .values(**fields))

        reading: SQLModel = await self.update_one(sql_statement=query, sql_model=reading)

        return cast(ReadingModel, reading)

    async def get_reading_by_id(self, reading_id, get_item: bool = False) -> ReadingModel | None:
        query = select(ReadingModel).where(ReadingModel.id == reading_id,
                                           ReadingModel.owner_id == self.user['user_id'])

        if get_item:
            query = query.options(joinedload(ReadingModel.item))

        reading: SQLModel = await self.get_only_one(query)

        return cast(ReadingModel, reading)

    async def get_readings(self, item_id) -> list[ReadingModel] | None:
        # Only the owner can get the readings
        # Maybe in future this can be a param, to get reading for someone the user want
        query = select(ReadingModel).where(
            ReadingModel.owner_id == self.user['user_id'],
            ReadingModel.item_id == item_id
            )

        query = query.order_by(ReadingModel.start_date.desc())

        readings = await self.get_all(query)

        return [reading['ReadingModel'] for reading in readings] if readings else None

    async def get_item_active_reading(self, item_id: int) -> ReadingModel | None:
        query = select(ReadingModel).where(ReadingModel.item_id == item_id, ReadingModel.active == True)

        reading: SQLModel = await self.get_only_one(query)

        return cast(ReadingModel, reading) if reading else None

    # Progress Methods
    async def create_progress(self, progress: SQLModel) -> ReadingProgressModel:
        new_progress = await self.add_one(progress)

        return cast(ReadingProgressModel, new_progress)

    async def update_progress(self, progress: SQLModel, fields: dict[str, Any]) -> ReadingProgressModel:
        query = (
            update(ReadingProgressModel)
            .where(ReadingProgressModel.id == progress.id)
            .values(**fields)
        )

        progress = await self.update_one(sql_statement=query, sql_model=progress)

        return cast(ReadingProgressModel, progress)

    async def get_progress(self, reading_id) -> list[ReadingProgressModel] | None:
        query = (select(ReadingProgressModel)
                .where(ReadingProgressModel.reading_id == reading_id)
                .order_by(ReadingProgressModel.date.desc()))

        progress_list = await self.get_all(query)

        return [progress['ReadingProgressModel'] for progress in progress_list] if progress_list else None

    async def get_latest_progress(self, reading_id) -> ReadingProgressModel | None:
        query = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id).order_by(ReadingProgressModel.date.desc())

        # TODO: get_first should return SQLModel!!
        latest_progress = await self.get_first(query)

        return latest_progress
