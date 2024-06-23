from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rolf_common.managers import BaseDataManager
from models import SQLModel, StatusModel
from models.item import ItemModel, ItemStatusModel
from schemas.request.item import CreateItemRequest
from datetime import datetime


class ItemManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_item(self, item: ItemModel) -> SQLModel:
        new_item = await self.add_one(item)

        return new_item

    async def get_item_by_id(self, item_id: int) -> SQLModel | None:
        stmt = select(ItemModel).where(ItemModel.id == item_id)

        item: SQLModel = await self.get_only_one(stmt)

        return item

    async def get_items(self) -> list[SQLModel] | None:
        stmt = select(ItemModel).order_by(ItemModel.id)

        items: list[SQLModel] = await self.get_all(stmt, unique_result=True)

        return items

    async def get_item_status_history(self, item_id: int) -> list[SQLModel] | None:
        stmt = select(ItemStatusModel).where(ItemStatusModel.item_id == item_id).order_by(ItemStatusModel.date.desc())

        item_status = await self.get_all(stmt)

        return item_status

