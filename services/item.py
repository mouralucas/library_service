from typing import Any

from starlette import status

from managers.item import ItemDataManager
from models import SQLModel, ItemModel
from schemas.item import ItemSchema
from schemas.request.item import GetItemRequest, CreateItemRequest
from schemas.response.item import GetItemResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.base import BaseService


class ItemService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_item(self, item: CreateItemRequest) -> Any:

        new_item = ItemDataManager(session=self.session).create_item(ItemModel(**item.dict()))


    async def get_items(self, params: GetItemRequest = None) -> GetItemResponse:
        items: list[SQLModel] = await ItemDataManager(self.session).get_items()

        a = [ItemSchema.model_validate(item) for item in items]

        response = GetItemResponse(
            quantity=len(items) if items else 0,
            status_code=status.HTTP_200_OK,
            items=a,
        )

        return response
