from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models.item import ItemModel
from schemas.item import ItemSchema


class ItemDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_item(self, item: ItemModel):
        new_item = self.add_one(item)

    async def get_item_by_id(self, item_id: int) -> BaseModel:
        stmt = select(ItemModel).where(ItemModel.id == item_id)

        item: BaseModel = await self.get_only_one(stmt)

        return item
