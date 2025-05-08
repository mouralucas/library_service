async def resolve_get_item(_, info, id):
    return {"id": id, "name": "Item do meu ovo" + id}


async def resolve_create_item(_, info, name):
    return {"id": "2", "name": name}


def bind_item_resolvers(query, mutation):
    query.set_field("getItem", resolve_get_item)
    mutation.set_field("createItem", resolve_create_item)
