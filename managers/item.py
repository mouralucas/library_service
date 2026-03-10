from typing import Any, cast

from fastapi import HTTPException
from rolf_common.managers import BaseDataManager
from sqlalchemy import RowMapping, asc, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
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
        query = select(ItemModel).where(ItemModel.id == item_id)

        item: SQLModel = await self.get_only_one(query)

        if not item and raise_exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")

        return cast(ItemModel, item)

    async def get_items(
        self,
        item_id: int | None = None,
        title: str | None = None,
        main_author_id: int | None = None,
        type: str | None = None,
        status_id: str | None = None,
        order_by: Any = None,
    ) -> list[dict[Any, Any]] | None:
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
                ItemModel.format.label("format_id"),
                ItemModel.type.label("item_type_id"),
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

        if type:
            query = query.where(ItemModel.type == type)

        if order_by:
            for item in order_by:
                column = getattr(ItemModel, item.field)
                if item.direction == "ASC":
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))

        items: list[RowMapping] | None = await self.get_all(query, unique_result=False)

        return [dict(i.items()) for i in items] if items else None

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
