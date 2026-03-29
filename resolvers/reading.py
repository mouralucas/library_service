from typing import Any

from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.reading import (
    CreateProgressRequestV2,
    CreateReadingGoalRequest,
    CreateReadingRequest,
    GetProgressRequest,
    GetReadingGoalsRquest,
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


@validate_graphql_input(CreateReadingRequest)
async def create_reading_resolver(_, info, reading: CreateReadingRequest):
    new_reading = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).create_reading(reading=reading)

    return new_reading


@validate_graphql_input(GetProgressRequest)
async def resolve_get_progress(_, info, params: GetProgressRequest) -> dict[str, Any]:
    progress = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_progress(params=params)

    return progress


@validate_graphql_input(CreateProgressRequestV2)
async def create_reading_progress_resolver(_, info, progress: CreateProgressRequestV2):
    new_progress = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).create_progress_v2(progress=progress)

    return new_progress


async def resolve_get_active_readings(_, info):
    readings = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_active_readings()

    return readings.model_dump(by_alias=True)


async def get_reading_stats_resolver(_, info, params) -> dict[str, Any]:
    params_ = GetReadingStatsRequest.model_validate(params)

    stats = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_reading_stats(params=params_)

    return stats


# Goals
@validate_graphql_input(CreateReadingGoalRequest)
async def create_reading_goal_resolver(_, info, goal: CreateReadingGoalRequest):
    new_goal = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).create_goal(goal=goal)

    return new_goal


@validate_graphql_input(GetReadingGoalsRquest)
async def get_reading_goals_resolver(_, info, params: GetReadingGoalsRquest):
    goals = await ReadingService(
        session=info.context["session"], user=info.context["user"]
    ).get_reading_goals(year=params.year)

    return goals


def bind_reading_resolvers(query, mutation):
    query.set_field("getReading", resolver=resolve_get_reading)
    query.set_field("getReadings", resolver=resolve_get_readings)
    query.set_field("getActiveReadings", resolver=resolve_get_active_readings)
    query.set_field("getReadingProgress", resolver=resolve_get_progress)
    query.set_field("getReadingStats", resolver=get_reading_stats_resolver)
    query.set_field("getReadingGoals", resolver=get_reading_goals_resolver)

    mutation.set_field("createReading", resolver=create_reading_resolver)
    mutation.set_field(
        "createReadingProgress", resolver=create_reading_progress_resolver
    )
    mutation.set_field("createReadingGoal", resolver=create_reading_goal_resolver)
