from schemas.request.item import GetItemRequest
from services.item import ItemService


async def resolve_get_item(_, info, id):
    item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_item_by_id(id)

    return item.model_dump(by_alias=True)


async def resolver_get_items(_, info, params):
    params_ = GetItemRequest.model_validate(params)

    items = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_items(params=params_)

    return items.model_dump(by_alias=True)


async def resolve_create_item(_, info, name):
    return {
        "id": "2",
        "name": name,
    }


def bind_item_resolvers(query, mutation):
    query.set_field("getItem", resolve_get_item)
    query.set_field("getItems", resolver_get_items)
    mutation.set_field("createItem", resolve_create_item)
