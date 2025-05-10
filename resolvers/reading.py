from schemas.request.reading import CreateReadingRequest
from schemas.response.reading import CreateReadingResponse
from services.reading import ReadingService


async def resolve_get_reading(_, info, id):
    return {"id": id, "name": "User " + id}


async def resolve_create_reading(_, info, reading):
    new_reading = CreateReadingRequest.model_validate(reading)

    new_reading = await ReadingService(session=info.context["session"], user=info.context["user"]).create_reading(reading=new_reading)
    return CreateReadingResponse.model_validate(new_reading)


def bind_reading_resolvers(query, mutation):
    query.set_field("getReading", resolve_get_reading)
    mutation.set_field("createReading", resolve_create_reading)
