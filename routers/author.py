from fastapi import APIRouter, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import get_session
from schemas.request.author import CreateAuthorRequest
from schemas.response.author import CreateAuthorResponse
from services.author import AuthorService

router = APIRouter(prefix="/author", tags=["Author"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(
    author: CreateAuthorRequest,
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> CreateAuthorResponse:
    response = await AuthorService(session).create_author(author=author)

    return response
