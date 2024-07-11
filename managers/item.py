from typing import Any

from sqlalchemy import select, update
from rolf_common.managers import BaseDataManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import SQLModel
from models.item import ItemModel, ItemStatusModel
from schemas.request.item import GetItemRequest


class ItemManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_item(self, item: ItemModel) -> SQLModel:
        new_item = await self.add_one(item)

        return new_item

    async def update_item(self, item: SQLModel, fields: dict[str, Any]) -> SQLModel:
        stmt = (
            update(ItemModel)
            .where(ItemModel.id == item.id)
            .values(**fields)
        )

        updated_item = await ItemManager(session=self.session).update_one(sql_statement=stmt, model=item)

        return updated_item

    async def get_item_by_id(self, item_id: int) -> SQLModel | None:
        stmt = select(ItemModel).where(ItemModel.id == item_id)

        item: SQLModel = await self.get_only_one(stmt)

        return item

    async def get_items(self, params: GetItemRequest) -> list[SQLModel] | None:
        stmt = select(ItemModel)

        for key, value in params.model_dump().items():
            if value:
                stmt = stmt.where(getattr(ItemModel, key) == value)

        stmt = stmt.order_by(ItemModel.id)

        items: list[SQLModel] = await self.get_all(stmt, unique_result=True)

        return items

    async def get_item_status_history(self, item_id: int) -> list[SQLModel] | None:
        stmt = select(ItemStatusModel).where(ItemStatusModel.item_id == item_id).order_by(ItemStatusModel.date.desc())

        item_status = await self.get_all(stmt)

        return item_status

