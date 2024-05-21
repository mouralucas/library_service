from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import db_session
from schemas.request.core import CreateLanguageRequest
from schemas.response.core import CreateLanguageResponse
from services.core import LanguageService

router = APIRouter(prefix='/core')


@router.post("/language", status_code=status.HTTP_201_CREATED)
async def create_language(language: CreateLanguageRequest,
                          session: AsyncSession = Depends(db_session)
                          ) -> CreateLanguageResponse:
    response = await LanguageService(session=session).create_language(language)

    return response


@router.get("/language")
async def get_language():
    pass
