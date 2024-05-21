from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import db_session
from schemas.request.core import CreateLanguageRequest, CreateCountryRequest
from schemas.response.core import CreateLanguageResponse, GetLanguageResponse, CreateCountryResponse, GetCountryResponse
from services.core import LanguageService, CountryService

router = APIRouter(prefix='/core')


@router.post("/language", status_code=status.HTTP_201_CREATED)
async def create_language(language: CreateLanguageRequest,
                          session: AsyncSession = Depends(db_session)
                          ) -> CreateLanguageResponse:
    response = await LanguageService(session=session).create_language(language)

    return response


@router.get("/language")
async def get_language(session: AsyncSession = Depends(db_session)) -> GetLanguageResponse:
    response = await LanguageService(session=session).get_languages()

    return response


@router.post("/country", status_code=status.HTTP_201_CREATED)
async def create_country(country: CreateCountryRequest,
                         session: AsyncSession = Depends(db_session)) -> CreateCountryResponse:
    response = await CountryService(session=session).create_country(country)

    return response


@router.get("/country")
async def get_country(session: AsyncSession = Depends(db_session)) -> GetCountryResponse:
    response = await CountryService(session=session).get_countries()

    return response

