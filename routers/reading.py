from fastapi import APIRouter, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import get_session
from schemas.request.reading import (
    CreateReadingRequest,
    GetProgressRequest,
    GetReadingStatsRequest,
)
from schemas.response.reading import (
    CreateReadingResponseV2,
    GetActiveReadingsResponse,
    GetProgressResponse,
    GetReadingStatsResponse,
)
from services.reading import ReadingService

router = APIRouter(prefix="/reading", tags=["Readings"])


@router.post(
    "",
    summary="Create a reading",
    description="Create a new reading for selected item",
    status_code=status.HTTP_201_CREATED,
)
async def create_reading(
    reading: CreateReadingRequest,
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> CreateReadingResponseV2:
    return await ReadingService(session=session, user=user).create_reading(
        reading=reading
    )


@router.get(
    "/active",
    summary="Get active readings",
    description="Get active readings for a item",
)
async def get_active_reading(
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> GetActiveReadingsResponse:
    # TODO: it need to add user param/filter
    response = await ReadingService(session=session, user=user).get_active_readings()

    return response


@router.get(
    "/stats", summary="Get reading stats", description="Get reading stats for a user"
)
async def get_reading_stats(
    params: GetReadingStatsRequest = Depends(),
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> GetReadingStatsResponse:
    return await ReadingService(session=session, user=user).get_reading_stats(
        params=params
    )


@router.get(
    "/progress",
    summary="Get progress",
    description="Get the progress for a reading",
    response_model_exclude_none=True,
)
async def get_reading_progress(
    params: GetProgressRequest = Depends(),
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> GetProgressResponse:
    # TODO: make accept item_id as param,
    #   than returns the progress for the last reading if more than one
    response = await ReadingService(session=session, user=user).get_progress(
        params=params
    )

    return response
