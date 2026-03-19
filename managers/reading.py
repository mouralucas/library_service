import datetime
import uuid
from typing import Any, cast

from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel
from sqlalchemy import RowMapping, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from models.core import StatusModel
from models.item import ItemModel
from models.reading import ReadingGoalModel, ReadingModel, ReadingProgressModel


class ReadingManager(BaseDataManager):
    def __init__(self, session: AsyncSession, user: dict[str, Any] = None):
        super().__init__(session=session)
        self.user = user

    async def create_reading(self, reading: ReadingModel) -> ReadingModel:
        new_reading: SQLModel = await self.add_one(reading)

        return cast(ReadingModel, new_reading)

    async def update_reading(
        self, reading: SQLModel, fields: dict[str, Any]
    ) -> ReadingModel:
        query = (
            update(ReadingModel).where(ReadingModel.id == reading.id).values(**fields)
        )

        updated_reading: SQLModel = await self.update_one(
            sql_statement=query, sql_model=reading
        )

        return cast(ReadingModel, updated_reading)

    async def get_reading_by_id(
        self, reading_id, get_item: bool = False
    ) -> ReadingModel | None:
        query = select(ReadingModel).where(
            ReadingModel.id == reading_id, ReadingModel.owner_id == self.user["user_id"]
        )

        if get_item:
            query = query.options(joinedload(ReadingModel.item))

        reading: SQLModel = await self.get_only_one(query)

        return cast(ReadingModel, reading)

    async def get_readings(
        self,
        item_id: int | None,
        reading_id: uuid.UUID | None = None,
        get_progress: bool = False,
    ) -> list[dict] | None:
        query = (
            select(
                ReadingModel.id,
                ReadingModel.owner_id,
                ReadingModel.active,
                ReadingModel.item_id,
                ItemModel.title.label("item_title"),
                ReadingModel.start_date,
                ReadingModel.finish_date,
                ReadingModel.number,
                ReadingModel.status_id,
                StatusModel.name.label("status_name"),
            )
            .join(StatusModel, ReadingModel.status_id == StatusModel.id)
            .join(ItemModel, ReadingModel.item_id == ItemModel.id)
            .where(
                ReadingModel.owner_id == self.user["user_id"],
            )
        )

        if item_id:
            query = query.where(ReadingModel.item_id == item_id)

        if reading_id:
            query = query.where(ReadingModel.id == reading_id)

        if get_progress:
            progress_alias = aliased(ReadingProgressModel)
            query = query.options(
                joinedload(ReadingModel.progress.of_type(progress_alias))
            ).order_by(progress_alias.progress_date.desc())

        query = query.order_by(ReadingModel.start_date.desc())

        readings = await self.get_all(query)

        return [dict(reading) for reading in readings] if readings else None

    async def get_item_last_readings(self, item_id: int) -> list[dict[str, Any]] | None:
        query = (
            select(
                ReadingModel.id,
                ReadingModel.owner_id,
                ReadingModel.active,
                ReadingModel.item_id,
                ItemModel.title.label("item_title"),
                ReadingModel.start_date,
                ReadingModel.finish_date,
                ReadingModel.number,
                ReadingModel.status_id,
                StatusModel.name.label("status_name"),
            )
            .join(StatusModel, ReadingModel.status_id == StatusModel.id)
            .join(ItemModel, ReadingModel.item_id == ItemModel.id)
            .where(
                ReadingModel.owner_id == self.user["user_id"],
                ReadingModel.item_id == item_id,
                ReadingModel.active == False,  # noqa: E712
            )
            .order_by(ReadingModel.finish_date.desc())
        )

        last_readings: list[RowMapping] | None = await self.get_all(query)

        return [dict(reading) for reading in last_readings] if last_readings else None

    async def get_all_active_readings(self) -> list[dict[Any, Any]] | None:
        query = (
            select(
                ReadingModel.id,
                ReadingModel.owner_id,
                ReadingModel.active,
                ReadingModel.item_id,
                ItemModel.title.label("item_title"),
                ReadingModel.start_date,
                ReadingModel.finish_date,
                ReadingModel.number,
                ReadingModel.status_id,
                StatusModel.name.label("status_name"),
                ReadingModel.created_at,
                ReadingModel.edited_at,
            )
            .join(ItemModel, ReadingModel.item_id == ItemModel.id)
            .join(StatusModel, ReadingModel.status_id == StatusModel.id)
            .where(ReadingModel.active, ReadingModel.owner_id == self.user["user_id"])
        )
        readings = await self.get_all(select_statement=query)

        return [dict(reading.items()) for reading in readings] if readings else None

    async def get_item_active_reading(self, item_id: int) -> ReadingModel | None:
        query = select(ReadingModel).where(
            ReadingModel.item_id == item_id, ReadingModel.active
        )

        reading: SQLModel | None = await self.get_only_one(query)

        return cast(ReadingModel, reading) if reading else None

    # Progress Methods
    async def create_progress(self, progress: SQLModel) -> ReadingProgressModel:
        new_progress = await self.add_one(progress)

        return cast(ReadingProgressModel, new_progress)

    async def update_progress(
        self, progress: SQLModel, fields: dict[str, Any]
    ) -> ReadingProgressModel:
        query = (
            update(ReadingProgressModel)
            .where(ReadingProgressModel.id == progress.id)
            .values(**fields)
        )

        progress = await self.update_one(sql_statement=query, sql_model=progress)

        return cast(ReadingProgressModel, progress)

    async def get_progress(self, reading_id) -> list[ReadingProgressModel] | None:
        query = (
            select(ReadingProgressModel)
            .where(ReadingProgressModel.reading_id == reading_id)
            .order_by(ReadingProgressModel.progress_date.desc())
        )

        progress_list = await self.get_all(query)

        return (
            [progress["ReadingProgressModel"] for progress in progress_list]
            if progress_list
            else None
        )

    async def get_latest_progress(self, reading_id) -> ReadingProgressModel | None:
        query = (
            select(ReadingProgressModel)
            .where(ReadingProgressModel.reading_id == reading_id)
            .order_by(ReadingProgressModel.progress_date.desc())
        )

        # TODO: get_first should return SQLModel!!
        latest_progress = await self.get_first(query)

        return cast(ReadingProgressModel, latest_progress)

    async def create_goal(self):
        # Can only create a goal for a item if not exist yet
        # Can a item be in the goal twice in same year?
        pass

    async def update_goal(
        self, goal: ReadingGoalModel, fields: dict[str, Any]
    ) -> ReadingGoalModel:
        query = (
            update(ReadingModel).where(ReadingGoalModel.id == goal.id).values(**fields)
        )

        updated_reading: SQLModel = await self.update_one(
            sql_statement=query, sql_model=goal
        )

        return cast(ReadingGoalModel, updated_reading)

    async def get_reading_goals(self, year: int | None):
        query = (
            select(
                ReadingGoalModel.id,
                ReadingGoalModel.item_id,
                ReadingGoalModel.acheived,
                ReadingGoalModel.date_acheived,
                ReadingGoalModel.year,
            )
            .where(ReadingGoalModel.owner_id == self.user["user_id"])
            .order_by(
                ReadingGoalModel.year,
                ReadingGoalModel.created_at.desc(),
            )
        )

        if year:
            query = query.where(ReadingGoalModel.year == year)

        goals = await self.get_all(query)

        return [dict(goal) for goal in goals] if goals else None

    async def get_active_goal_by_item_id(self, item_id: int) -> ReadingGoalModel | None:
        """
        :Created by: Lucas Penha de Moura - 17/03/2026
            Get the active goal for a item (not achieved yet)

            Params:
                item_id: the id of the item
        """
        query = select(
            ReadingGoalModel.id,
            ReadingGoalModel.item_id,
            ReadingGoalModel.acheived,
            ReadingGoalModel.date_acheived,
            ReadingGoalModel.year,
        ).where(
            ReadingGoalModel.owner_id == self.user["user_id"],
            ReadingGoalModel.item_id == item_id,
            ReadingGoalModel.acheived.is_(False),
            ReadingGoalModel.year == datetime.datetime.now().year,
        )

        goal = await self.get_only_one(query)

        return cast(ReadingGoalModel, goal) if goal else None
