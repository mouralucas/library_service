from typing import Any

from fastapi import APIRouter, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from services.reading import ReadingService

router = APIRouter(prefix="/reading", tags=["Readings"])


@router.get(
    "/active",
    summary="Get active readings",
    description="Get active readings for a item",
)
async def get_active_reading(
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> dict[str, Any]:
    # TODO: it need to add user param/filter
    response = await ReadingService(session=session, user=user).get_active_readings()

    return response
