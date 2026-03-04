from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import get_session
from schemas.request.core import (
    CreateCollectionRequest,
    CreateCountryRequest,
    CreateLanguageRequest,
    CreatePublisherRequest,
    CreateSerieRequest,
)
from schemas.response.core import (
    CreateCollectionResponse,
    CreateCountryResponse,
    CreateLanguageResponse,
    CreatePublisherResponse,
    CreateSerieResponse,
    GetCountryResponse,
)
from services.core import (
    CollectionService,
    CountryService,
    LanguageService,
    PublisherService,
    SerieService,
)

router = APIRouter(prefix="", tags=["Base"])


@router.post("/language", status_code=status.HTTP_201_CREATED)
async def create_language(
    language: CreateLanguageRequest, session: AsyncSession = Depends(get_session)
) -> CreateLanguageResponse:
    response = await LanguageService(session=session).create_language(language)

    return response


@router.post("/country", status_code=status.HTTP_201_CREATED)
async def create_country(
    country: CreateCountryRequest, session: AsyncSession = Depends(get_session)
) -> CreateCountryResponse:
    response = await CountryService(session=session).create_country(country)

    return response


@router.get("/country")
async def get_country(
    session: AsyncSession = Depends(get_session),
) -> GetCountryResponse:
    response = await CountryService(session=session).get_countries()

    return response


@router.post("/collection", status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: CreateCollectionRequest, session: AsyncSession = Depends(get_session)
) -> CreateCollectionResponse:
    response = await CollectionService(session=session).create_collection(collection)

    return response


@router.post("/publisher", status_code=status.HTTP_201_CREATED)
async def create_publisher(
    publisher: CreatePublisherRequest, session: AsyncSession = Depends(get_session)
) -> CreatePublisherResponse:
    response = await PublisherService(session).create_publisher(publisher)

    return response
