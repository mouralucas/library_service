from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import db_session
from schemas.request.author import CreateAuthorRequest
from schemas.response.author import GetAuthorResponse, CreateAuthorResponse
from services.service import AuthorService

router = APIRouter(prefix="/author")


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_author(author: CreateAuthorRequest,
                        session: AsyncSession = Depends(db_session)) -> CreateAuthorResponse:
    response = await AuthorService(session).create_author(author=author)

    return response


@router.get('')
async def get_authors(session: AsyncSession = Depends(db_session)) -> GetAuthorResponse:
    response = await AuthorService(session).get_author()

    return response
