from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.reading import (
    CreateProgressRequestV2,
    CreateReadingRequest,
    GetProgressRequest,
    GetReadingRequest,
    GetReadingStatsRequest,
)
from services.reading import ReadingService


async def resolve_get_reading(_, info, reading_id):
    reading = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_reading_by_id(reading_id)

    return reading.model_dump(by_alias=True)


@validate_graphql_input(GetReadingRequest)
async def resolve_get_readings(_, info, params: GetReadingRequest):
    readings = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_readings(
        item_id=params.item_id,
        reading_id=params.reading_id,
        get_progress=params.get_progress,
    )

    return readings


async def create_reading_resolver(_, info, reading):
    new_reading = CreateReadingRequest.model_validate(reading)

    new_reading = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).create_reading(reading=new_reading)

    return new_reading.model_dump(by_alias=True)


async def resolve_get_progress(_, info, params):
    progress = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_progress(params=GetProgressRequest.model_validate(params))

    return progress.model_dump(by_alias=True)


async def create_reading_progress_resolver(_, info, progress):
    new_progress_ = CreateProgressRequestV2.model_validate(progress)

    new_progress = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).create_progress_v2(progress=new_progress_)

    return new_progress


async def resolve_get_active_readings(_, info):
    readings = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_active_readings()

    return readings.model_dump(by_alias=True)


async def get_reading_stats_resolver(_, info, params):
    params_ = GetReadingStatsRequest.model_validate(params)

    stats = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_reading_stats(params=params_)

    return stats.model_dump(by_alias=True)


def bind_reading_resolvers(query, mutation):
    query.set_field("getReading", resolver=resolve_get_reading)
    query.set_field("getReadings", resolver=resolve_get_readings)
    query.set_field("getActiveReadings", resolver=resolve_get_active_readings)
    query.set_field("getReadingProgress", resolver=resolve_get_progress)
    query.set_field("getReadingStats", resolver=get_reading_stats_resolver)

    mutation.set_field("createReading", resolver=create_reading_resolver)
    mutation.set_field(
        "createReadingProgress", resolver=create_reading_progress_resolver
    )
