from typing import Any, cast

from fastapi import HTTPException
from rolf_common.managers import BaseDataManager
from sqlalchemy import RowMapping, func, select, update
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
from models.item import ItemModel, ItemStatusModel
from schemas.request.item import GetItemRequest


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

    async def get_items(self, params: GetItemRequest) -> list[dict[Any, Any]] | None:
        query = (
            select(
                ItemModel.id,
                ItemModel.owner_id,
                ItemModel.title,
                ItemModel.subtitle,
                ItemModel.title_original,
                ItemModel.subtitle_original,
                ItemModel.pages,
                ItemModel.publication_date,
                ItemModel.original_publication_date,
                ItemModel.edition,
                ItemModel.serie_id,
                SerieModel.name.label("serie_name"),
                ItemModel.language_id,
                ItemModel.volume,
                ItemModel.isbn,
                ItemModel.isbn10,
                ItemModel.publisher_id,
                PublisherModel.name.label("publisher_name"),
                ItemModel.main_author_id,
                AuthorModel.name.label("main_author_name"),
                ItemModel.collection_id,
                CollectionModel.name.label("collection_name"),
                ItemModel.format,
                ItemModel.type,
                ItemModel.last_status_id,
                StatusModel.name.label("last_status_name"),
                ItemModel.last_status_date,
                ItemModel.cover_price,
                ItemModel.paid_price,
                ItemModel.dimensions,
                ItemModel.height,
                ItemModel.width,
                ItemModel.thickness,
                ItemModel.summary,
                ItemModel.observation,
            )
            .join(AuthorModel, ItemModel.main_author_id == AuthorModel.id)
            .join(SerieModel, ItemModel.serie_id == SerieModel.id)
            .join(CollectionModel, ItemModel.collection_id == CollectionModel.id)
            .outerjoin(PublisherModel, ItemModel.publisher_id == PublisherModel.id)
            .join(StatusModel, ItemModel.last_status_id == StatusModel.id)
        )

        for key, value in params.model_dump().items() if params else []:
            if value:
                # TODO: Make this function better!!
                attr = getattr(ItemModel, key)
                if attr == ItemModel.title:
                    query = query.where(func.lower(attr).like(f"%{value.lower()}%"))
                else:
                    query = query.where(attr == value)

        query = query.order_by(ItemModel.id)

        items: list[RowMapping] | None = await self.get_all(query, unique_result=True)

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
