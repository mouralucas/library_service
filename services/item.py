from typing import Any

from rolf_common.schemas.auth import RequiredUser
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.item import ItemManager
from models import SQLModel, ItemModel, ItemStatusModel, ItemAuthorModel
from schemas.item import ItemSchema
from schemas.request.item import GetItemRequest, CreateItemRequest, UpdateItemRequest
from schemas.response.item import GetItemResponse, CreateItemResponse
from services.base import BaseService


class ItemService(BaseService):
    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()

    async def create_item(self, item: CreateItemRequest) -> CreateItemResponse:
        # TODO: I did not like this, improve
        item.owner_id = self.user['user_id']

        new_item = await ItemManager(session=self.session).create_item(
            ItemModel(**item.model_dump(exclude={'other_authors_id'})))

        await self.__update_status(new_item)
        await self.__add_author(item_id=new_item.id, main_author_id=item.main_author_id,
                                other_authors_id=item.other_authors_id)

        await self.session.refresh(new_item)

        response = CreateItemResponse(
            status_code=status.HTTP_201_CREATED,
            item=ItemSchema.model_validate(new_item)
        )

        return response

    async def update_item(self, item: UpdateItemRequest) -> CreateItemResponse:
        current_item = await ItemManager(self.session).get_item_by_id(item_id=item.id)

        clean_item_fields = item.model_dump(exclude={'other_authors_id'}, exclude_unset=True)
        updated_item = await ItemManager(session=self.session).update_item(current_item, fields=clean_item_fields)

        if clean_item_fields.get('last_status_id'):
            await self.__update_status(updated_item)

        if clean_item_fields.get('main_author_id') or clean_item_fields.get('other_authors_id'):
            pass

        await self.session.refresh(updated_item)

        # TODO: add validation if author(s) were changed, if so add correspondent method

        response = CreateItemResponse(
            item=ItemSchema.model_validate(updated_item)
        )

        return response

    async def get_items(self, params: GetItemRequest = None) -> GetItemResponse:
        items: list[dict[str, Any]] = await ItemManager(self.session).get_items(params)

        response = GetItemResponse(
            quantity=len(items) if items else 0,
            items=[ItemSchema.model_validate(item) for item in items] if items else None,
        )

        return response

    async def __update_status(self, item: ItemModel, is_update: bool = False):
        """
        :Name: __update_status
        :Created by: Lucas Penha de Moura - 22/06/2024
            Update the status history for a item

        :Params:
            serie: the ItemModel object
        """
        status_history = await ItemManager(session=self.session).get_item_status_history(item.id)

        status_history = status_history[0] if status_history else None

        if not status_history or (status_history.status_id != item.last_status_id):
            new_status = ItemStatusModel(
                item_id=item.id,
                status_id=item.last_status_id,
                date=item.last_status_date,
            )
            await ItemManager(session=self.session).add_one(new_status)

        return

    async def __add_author(self, item_id, main_author_id: int, other_authors_id: list[int] = None):
        """
        :Name: __add_author
        :Created by: Lucas Penha de Moura - 23/06/2024
            Create the relation for item and authors.

        :Params:
            item_id: the id of the item
            main_author_id: the id of the main author
            other_authors_id: the ids of the other authors
        """
        main_author = ItemAuthorModel(
            item_id=item_id,
            author_id=main_author_id,
        )
        await ItemManager(session=self.session).add_one(main_author)

        other_authors = []
        for author_id in other_authors_id if other_authors_id else []:
            author = ItemAuthorModel(
                item_id=item_id,
                author_id=author_id,
                is_main=False
            )
            other_authors.append(author)

        if other_authors:
            await ItemManager(self.session).add_all(other_authors)

        return
