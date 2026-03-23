from typing import Any

from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.item import (
    CreateItemRequest,
    GetItemRequest,
    GetItemSummaryRequest,
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


@validate_graphql_input(CreateItemRequest)
async def create_item_resolver(_, info, item: CreateItemRequest):

    new_item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).create_item(item=item)

    return new_item


@validate_graphql_input(UpdateItemRequest)
async def update_item_resolver(_, info, item: UpdateItemRequest):
    updated_item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).update_item(item=item)

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


@validate_graphql_input(GetItemSummaryRequest)
async def get_item_summary(_, info, params: GetItemSummaryRequest):
    summary = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_item_summary(params=params)
    return summary


def bind_item_resolvers(query, mutation):
    query.set_field("getItems", get_items_resolver)
    query.set_field("getItemSummary", resolver=get_item_summary)
    query.set_field("getItemLocations", get_item_locations_resolver)
    query.set_field("getItemsByLocation", get_items_by_location_resolver)

    mutation.set_field("createItem", create_item_resolver)
    mutation.set_field("updateItem", update_item_resolver)
