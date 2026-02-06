from fastapi import APIRouter, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import get_session
from schemas.request.core import (
    CreateCollectionRequest,
    CreateCountryRequest,
    CreateLanguageRequest,
    CreatePublisherRequest,
    CreateSerieRequest,
    GetStatusRequest,
)
from schemas.response.core import (
    CreateCollectionResponse,
    CreateCountryResponse,
    CreateLanguageResponse,
    CreatePublisherResponse,
    CreateSerieResponse,
    GetCollectionResponse,
    GetCountryResponse,
    GetLanguageResponse,
    GetPublisherResponse,
    GetSeriesResponse,
    GetStatusResponse,
)
from services.core import (
    CollectionService,
    CountryService,
    LanguageService,
    PublisherService,
    SerieService,
    StatusService,
)

router = APIRouter(prefix="", tags=["Base"])


@router.post("/language", status_code=status.HTTP_201_CREATED)
async def create_language(
    language: CreateLanguageRequest, session: AsyncSession = Depends(get_session)
) -> CreateLanguageResponse:
    response = await LanguageService(session=session).create_language(language)

    return response


@router.get("/language")
async def get_language(
    session: AsyncSession = Depends(get_session),
) -> GetLanguageResponse:
    response = await LanguageService(session=session).get_languages()

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


@router.post("/serie", status_code=status.HTTP_201_CREATED)
async def create_serie(
    serie: CreateSerieRequest, session: AsyncSession = Depends(get_session)
) -> CreateSerieResponse:
    response = await SerieService(session=session).create_serie(serie)

    return response


@router.get("/serie")
async def get_serie(session: AsyncSession = Depends(get_session)) -> GetSeriesResponse:
    response = await SerieService(session=session).get_series()

    return response


@router.post("/collection", status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: CreateCollectionRequest, session: AsyncSession = Depends(get_session)
) -> CreateCollectionResponse:
    response = await CollectionService(session=session).create_collection(collection)

    return response


@router.get("/collection")
async def get_collection(
    session: AsyncSession = Depends(get_session),
) -> GetCollectionResponse:
    response = await CollectionService(session=session).get_collections()

    return response


@router.post("/publisher", status_code=status.HTTP_201_CREATED)
async def create_publisher(
    publisher: CreatePublisherRequest, session: AsyncSession = Depends(get_session)
) -> CreatePublisherResponse:
    response = await PublisherService(session).create_publisher(publisher)

    return response


@router.get("/publisher")
async def get_publisher(
    session: AsyncSession = Depends(get_session),
) -> GetPublisherResponse:
    response = await PublisherService(session).get_publishers()

    return response
