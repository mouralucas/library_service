from schemas.request.reading import CreateReadingRequest
from services.reading import ReadingService


async def resolve_get_reading(_, info, reading_id):
    reading = await ReadingService(session=info.context["session"], user=info.context["user"]).get_reading_by_id(reading_id)

    return reading.model_dump()


async def resolve_get_readings(_, info):
    readings = await ReadingService(session=info.context["session"], user=info.context["user"]).get_readings()

    return readings.model_dump()


async def resolve_create_reading(_, info, reading):
    new_reading = CreateReadingRequest.model_validate(reading)

    new_reading = await ReadingService(session=info.context["session"], user=info.context["user"]).create_reading(reading=new_reading)
    return new_reading.model_dump()


def bind_reading_resolvers(query, mutation):
    query.set_field("getReading", resolve_get_reading)
    query.set_field("getReadings", resolve_get_readings)
    mutation.set_field("createReading", resolve_create_reading)
