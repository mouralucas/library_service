from schemas.request.item import CreateItemRequest, GetItemRequest
from services.item import ItemService


async def resolve_get_item(_, info, id):
    item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_item_by_id(id)

    return item.model_dump(by_alias=True)


async def get_items_resolver(_, info, params):
    params_ = GetItemRequest.model_validate(params)

    items = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).get_items(params=params_)

    return items.model_dump(by_alias=True)


async def create_item_resolver(_, info, item):
    item_ = CreateItemRequest.model_validate(item)

    new_item = await ItemService(
        session=info.context["session"], user=info.context["user"]
    ).create_item(item=item_)

    return new_item.model_dump(by_alias=True)


def bind_item_resolvers(query, mutation):
    query.set_field("getItem", resolve_get_item)
    query.set_field("getItems", get_items_resolver)

    mutation.set_field("createItem", create_item_resolver)
