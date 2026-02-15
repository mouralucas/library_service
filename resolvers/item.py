from typing import Any

from schemas.request.item import CreateItemRequest, GetItemRequest, UpdateItemRequest
from services.item import ItemService


async def get_items_resolver(_, info, params):
    params_ = GetItemRequest.model_validate(params)

    items = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_items(params=params_)

    return items


async def create_item_resolver(_, info, item):
    item_ = CreateItemRequest.model_validate(item)

    new_item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).create_item(item=item_)

    return new_item


async def update_item_resolver(_, info, item):
    item_ = UpdateItemRequest.model_validate(item)

    updated_item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).update_item(item=item_)

    return updated_item.model_dump(by_alias=True)


async def get_item_locations_resolver(_, info) -> dict[str, Any]:
    locations = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_item_locations()

    return locations


def bind_item_resolvers(query, mutation):
    query.set_field("getItems", get_items_resolver)
    query.set_field("getItemLocations", get_item_locations_resolver)

    mutation.set_field("createItem", create_item_resolver)
    mutation.set_field("updateItem", update_item_resolver)
