from typing import Any

from starlette import status

from managers.core import StatusManager
from managers.item import ItemManager
from models import SQLModel, ItemModel, ItemStatusModel
from schemas.item import ItemSchema
from schemas.request.item import GetItemRequest, CreateItemRequest
from schemas.response.item import GetItemResponse, CreateItemResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.base import BaseService

from datetime import datetime


class ItemService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_item(self, item: CreateItemRequest) -> CreateItemResponse:
        new_item = await ItemManager(session=self.session).create_item(ItemModel(**item.model_dump(exclude={'other_authors_id'})))

        await self.__update_status(new_item)

        response = CreateItemResponse(
            status_code=status.HTTP_201_CREATED,
            item=ItemSchema.model_validate(new_item)
        )

        return response

    async def get_items(self, params: GetItemRequest = None) -> GetItemResponse:
        items: list[SQLModel] = await ItemManager(self.session).get_items()

        response = GetItemResponse(
            quantity=len(items) if items else 0,
            status_code=status.HTTP_200_OK,
            items=[ItemSchema.model_validate(item) for item in items] if items else [],
        )

        return response

    async def __update_status(self, item: SQLModel, is_update: bool = False):
        status_history = await ItemManager(session=self.session).get_item_status_history(item.id)

        status_history = status_history[0] if status_history else None

        if not status_history or status_history.status_id != item.last_status_id:
            new_status = ItemStatusModel(
                item_id=item.id,
                status_id=item.last_status_id,
                date=item.last_status_date,
            )
            await ItemManager(session=self.session).add_one(new_status)

        return
