from typing import Any, cast

from fastapi import HTTPException
from sqlalchemy import select, update, func, RowMapping
from rolf_common.managers import BaseDataManager
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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

        updated_item = await self.update_one(sql_statement=stmt, sql_model=item)

        return updated_item

    async def get_item_by_id(self, item_id: int, raise_exception: bool = False) -> SQLModel | None:
        stmt = select(ItemModel).where(ItemModel.id == item_id)

        item: SQLModel = await self.get_only_one(stmt)

        if not item and raise_exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Item not found')

        return item

    async def get_items(self, params: GetItemRequest) -> list[ItemModel] | None:
        stmt = select(ItemModel)

        for key, value in params.model_dump().items():
            if value:
                # TODO: Make this function better!!
                attr = getattr(ItemModel, key)
                if attr == ItemModel.title:
                    stmt = stmt.where(func.lower(attr).like(f"%{value.lower()}%"))
                else:
                    stmt = stmt.where(attr == value)


        stmt = stmt.order_by(ItemModel.id)

        items: list[RowMapping] = await self.get_all(stmt, unique_result=True)

        return [cast(ItemModel, item) for item in items] if items else None

    async def get_item_status_history(self, item_id: int) -> list[ItemStatusModel] | None:
        stmt = select(ItemStatusModel).where(ItemStatusModel.item_id == item_id).order_by(ItemStatusModel.date.desc())

        item_status = await self.get_all(stmt)

        return [item['ItemStatusModel'] for item in item_status] if item_status else None

