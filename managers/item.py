from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models import SQLModel
from models.item import ItemModel


class ItemDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_item(self, item: ItemModel):
        new_item = self.add_one(item)

        return new_item

    async def get_item_by_id(self, item_id: int) -> BaseModel | None:
        stmt = select(ItemModel).where(ItemModel.id == item_id)

        item: BaseModel = await self.get_only_one(stmt)

        return item

    async def get_items(self) -> list[SQLModel] | None:
        stmt = select(ItemModel).order_by(ItemModel.id)

        items: list[SQLModel] = await self.get_all(stmt, unique_result=True)

        return items
