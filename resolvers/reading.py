async def resolve_get_reading(_, info, id):
    return {"id": id, "name": "User " + id}


async def resolve_create_reading(_, info, name):
    return {"id": "1", "name": name}


def bind_reading_resolvers(query, mutation):
    query.set_field("getReading", resolve_get_reading)
    mutation.set_field("createReading", resolve_create_reading)
