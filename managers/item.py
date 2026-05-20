import datetime
from typing import Any, cast

from fastapi import HTTPException
from rolf_common.managers import BaseDataManager
from sqlalchemy import RowMapping, asc, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from starlette import status

from models import (
    AuthorModel,
    CollectionModel,
    PublisherModel,
    SerieModel,
    SQLModel,
    StatusModel,
)
from models.item import ItemAuthorModel, ItemLocationModel, ItemModel, ItemStatusModel
from models.reading import ReadingModel, ReadingProgressModel, ReadingQueueModel


class ItemManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_item(self, item: ItemModel) -> ItemModel:
        new_item = await self.add_one(item)

        return cast(ItemModel, new_item)

    async def update_item(self, item: SQLModel, fields: dict[str, Any]) -> ItemModel:
        query = update(ItemModel).where(ItemModel.id == item.id).values(**fields)

        updated_item = await self.update_one(sql_statement=query, sql_model=item)

        return cast(ItemModel, updated_item)

    async def get_item_by_id(
        self, item_id: int, raise_exception: bool = False
    ) -> ItemModel | None:
        """
        :Name:  get_item_by_id
        :Created by: Lucas Penha de Moura - 03/04/2024
            Get an item by its ID.

            The method returns the Item object, without any relation.
            If the item is not found, it returns None or raises an exception
                if raise_exception is True.

        Params:
            item_id: the ID of the item to retrieve
        """
        query = select(ItemModel).where(ItemModel.id == item_id)

        item: SQLModel | None = await self.get_only_one(query)

        if not item and raise_exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

        return cast(ItemModel, item)

    async def get_detailed_items(
        self,
        item_id: int | None = None,
        title: str | None = None,
        main_author_id: int | None = None,
        item_type_id: str | None = None,
        status_id: str | None = None,
        id_list: list[int] | None = None,
        order_by: Any = None,
    ) -> list[dict[Any, Any]] | None:
        """
        :Name:  get_detailed_items
        :Created by: Lucas Penha de Moura - 03/04/2024
            Get detailed information about items.

            The method returns a list of dictionaries containing
                the detailed item information.
            If no items are found, it returns an empty list.

        Params:
            item_id: the ID of the item to retrieve
            title: the title of the item to retrieve
            main_author_id: the ID of the main author of the item to retrieve
            item_type_id: the type of the item to retrieve
            status_id: the status of the item to retrieve
            id_list: a list of item IDs to retrieve
            order_by: a list of dict with field and direction to order the result
        """
        reading_queue_exists = (
            select(1)
            .where(
                ReadingQueueModel.item_id == ItemModel.id,
                ReadingQueueModel.owner_id == ItemModel.owner_id,
                ReadingQueueModel.active.is_(True),
                ReadingQueueModel.year == datetime.datetime.now().year,
            )
            .exists()
        )

        authors_subq = (
            select(
                ItemAuthorModel.item_id.label("item_id"),
                func.array_agg(func.distinct(AuthorModel.id)).label("authors_ids"),
                func.array_agg(func.distinct(AuthorModel.name)).label("authors_names"),
            )
            .where(ItemAuthorModel.is_main.is_(False))
            .join(AuthorModel, AuthorModel.id == ItemAuthorModel.author_id)
            .group_by(ItemAuthorModel.item_id)
        ).subquery()

        query = (
            select(
                ItemModel.id,
                ItemModel.owner_id,
                ItemModel.title,
                ItemModel.subtitle,
                ItemModel.pages,
                ItemModel.publication_date,
                ItemModel.original_publication_date,
                ItemModel.serie_id,
                SerieModel.name.label("serie_name"),
                ItemModel.language_id,
                ItemModel.volume,
                ItemModel.isbn,
                ItemModel.publisher_id,
                PublisherModel.name.label("publisher_name"),
                ItemModel.main_author_id,
                AuthorModel.name.label("main_author_name"),
                ItemModel.collection_id,
                CollectionModel.name.label("collection_name"),
                ItemModel.format_id.label("format_id"),
                ItemModel.item_type_id.label("item_type_id"),
                ItemModel.last_status_id,
                StatusModel.name.label("last_status_name"),
                ItemModel.last_status_date,
                ItemModel.cover_price,
                ItemModel.paid_price,
                ItemModel.cover,
                ItemModel.summary,
                ItemModel.observation,
                ItemModel.location_id,
                authors_subq.c.authors_ids,
                authors_subq.c.authors_names,
                reading_queue_exists.label("is_in_reading_queue"),
            )
            .join(AuthorModel, ItemModel.main_author_id == AuthorModel.id)
            .outerjoin(SerieModel, ItemModel.serie_id == SerieModel.id)
            .outerjoin(PublisherModel, ItemModel.publisher_id == PublisherModel.id)
            .join(CollectionModel, ItemModel.collection_id == CollectionModel.id)
            .join(StatusModel, ItemModel.last_status_id == StatusModel.id)
            .outerjoin(authors_subq, authors_subq.c.item_id == ItemModel.id)
        )

        if item_id:
            query = query.where(ItemModel.id == item_id)

        if title:
            query = query.where(ItemModel.title == title)

        if main_author_id:
            query = query.where(ItemModel.main_author_id == main_author_id)

        if status_id:
            query = query.where(ItemModel.last_status_id == status_id)

        if item_type_id:
            query = query.where(ItemModel.item_type_id == item_type_id)

        if id_list:
            query = query.where(ItemModel.id.in_(id_list))

        if order_by:
            for item in order_by:
                column = getattr(ItemModel, item.field)
                if item.direction == "ASC":
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))

        items: list[RowMapping] | None = await self.get_all(query, unique_result=False)

        return [dict(i.items()) for i in items] if items else None

    async def get_item_summary(
        self,
        item_id: int | None = None,
        item_type_id: str | None = None,
        active_goal: bool = False,
        active_reading: bool = False,
        order_by: Any = None,
    ) -> list[dict[Any, Any]] | None:
        """
        :Created by: Lucas Penha de Moura - 19/03/2026
            Fetch the current state of an item

            Params:
                itemId: the id of the item
                itemTypeId: the type of the item
                active_goal: if true, return only items with active reading goal
                    for the current year
                active_reading: if true, return only items with active reading
                order_by: a list of dict with field and direction to order the result
        """
        # TODO: if this query start to be a bottleneck try Materialized view or
        #   something similar
        current_year = datetime.datetime.now().year

        # --- Subquery: Current year ReadingGoal ---
        reading_goal_subq = (
            select(
                ReadingQueueModel.id,
                ReadingQueueModel.year,
                ReadingQueueModel.achieved,
                ReadingQueueModel.item_id,
                ReadingQueueModel,
            )
            .where(
                ReadingQueueModel.year == current_year,
                ReadingQueueModel.active.is_(True),
            )
            .subquery()
        )

        # --- Subquery: Last Reading fot the item ---
        reading_subq = select(
            ReadingModel.id,
            ReadingModel.item_id,
            ReadingModel.start_date,
            func.row_number()
            .over(
                partition_by=ReadingModel.item_id,
                order_by=ReadingModel.start_date.desc(),
            )
            .label("rn"),
        ).subquery()

        latest_reading = aliased(reading_subq)

        # --- Subquery: Last ReadingProgress for the last Reading ---
        progress_subq = select(
            ReadingProgressModel.reading_id,
            ReadingProgressModel.page,
            ReadingProgressModel.percentage,
            ReadingProgressModel.progress_date,
            func.row_number()
            .over(
                partition_by=ReadingProgressModel.reading_id,
                order_by=ReadingProgressModel.progress_date.desc(),
            )
            .label("rn"),
        ).subquery()

        latest_progress = aliased(progress_subq)

        # --- Main Query ---
        query = (
            select(
                ItemModel.id,
                ItemModel.title,
                ItemModel.cover,
                ItemModel.main_author_id,
                AuthorModel.name.label("main_author_name"),
                # Goal
                reading_goal_subq.c.id.label("reading_goal_id"),
                reading_goal_subq.c.year.label("reading_goal_year"),
                reading_goal_subq.c.achieved.label("reading_goal_achieved"),
                # Latest Reading
                latest_reading.c.id.label("reading_id"),
                latest_reading.c.start_date.label("reading_start_date"),
                # Latest Progress
                latest_progress.c.page.label("last_page"),
                latest_progress.c.percentage.label("last_percentage"),
            )
            # Goal
            .outerjoin(
                reading_goal_subq,
                ItemModel.id == reading_goal_subq.c.item_id,
            )
            .outerjoin(
                latest_reading,
                (latest_reading.c.item_id == ItemModel.id) & (latest_reading.c.rn == 1),
            )
            .outerjoin(
                latest_progress,
                (latest_progress.c.reading_id == latest_reading.c.id)
                & (latest_progress.c.rn == 1),
            )
            .outerjoin(AuthorModel, AuthorModel.id == ItemModel.main_author_id)
        )

        if item_id:
            query = query.where(ItemModel.id == item_id)

        if item_type_id:
            query = query.where(ItemModel.item_type_id == item_type_id)

        if active_goal:
            query = query.where(reading_goal_subq.c.id.is_not(None))

        if active_reading:
            query = query.outerjoin(
                ReadingModel,
                (ReadingModel.item_id == ItemModel.id)
                & (ReadingModel.active.is_(True)),
            )
            query = query.where(ReadingModel.id.is_not(None))

        if order_by:
            for item in order_by:
                column = getattr(ItemModel, item.field)
                if item.direction == "ASC":
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))

        items = await self.get_all(query)

        return [dict(location.items()) for location in items] if items else None

    async def get_item_status_history(
        self, item_id: int
    ) -> list[ItemStatusModel] | None:
        stmt = (
            select(ItemStatusModel)
            .where(ItemStatusModel.item_id == item_id)
            .order_by(ItemStatusModel.date.desc())
        )

        item_status = await self.get_all(stmt)

        return (
            [item["ItemStatusModel"] for item in item_status] if item_status else None
        )

    async def get_item_locations(self) -> list[dict[Any, Any]] | None:
        query = select(
            ItemLocationModel.id,
            ItemLocationModel.name,
            ItemLocationModel.physical_location,
            ItemLocationModel.description,
        ).order_by(ItemLocationModel.name.asc())

        locations: list[RowMapping] | None = await self.get_all(
            query, unique_result=True
        )

        return [dict(location.items()) for location in locations] if locations else None

    async def get_items_by_location(
        self, location_ids: list[int] | None = None
    ) -> list[dict[Any, Any]] | None:
        query = select(
            ItemModel.id,
            ItemModel.title,
            ItemModel.main_author_id,
            ItemModel.cover,
            ItemLocationModel.id.label("location_id"),
            ItemLocationModel.name.label("location_name"),
            ItemLocationModel.physical_location,
            ItemLocationModel.description.label("location_description"),
        ).join(ItemLocationModel, ItemModel.location_id == ItemLocationModel.id)

        if location_ids:
            query = query.where(ItemModel.location_id.in_(location_ids))

        items: list[RowMapping] | None = await self.get_all(query, unique_result=True)

        return [dict(item.items()) for item in items] if items else None

    async def get_items_indexed(self, items: list[dict[str, Any]] | None):
        """
        :Name: create_author
        :Created by: Lucas Penha de Moura - 17/03/2026
            This method creates a mapper for items, item returns indexed by item Id

            Params:
                item: a list of items
        """
        mapped_items = {item["id"]: item for item in items} if items else {}

        return mapped_items
