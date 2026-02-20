from typing import Any

from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.item import (
    CreateItemRequest,
    GetItemRequest,
    GetItemsByLocationRequest,
    UpdateItemRequest,
)
from services.item import ItemService


@validate_graphql_input(GetItemRequest)
async def get_items_resolver(_, info, params: GetItemRequest):
    items = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_items(params=params)

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


@validate_graphql_input(GetItemsByLocationRequest)
async def get_items_by_location_resolver(_, info, params: GetItemsByLocationRequest):
    items = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_items_by_location(location_ids=params.location_ids)

    return items


def bind_item_resolvers(query, mutation):
    query.set_field("getItems", get_items_resolver)
    query.set_field("getItemLocations", get_item_locations_resolver)
    query.set_field("getItemsByLocation", get_items_by_location_resolver)

    mutation.set_field("createItem", create_item_resolver)
    mutation.set_field("updateItem", update_item_resolver)
