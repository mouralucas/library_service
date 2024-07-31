from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import db_session
from schemas.request.core import CreateLanguageRequest, CreateCountryRequest, CreateSerieRequest, CreateCollectionRequest, CreatePublisherRequest
from schemas.response.core import CreateLanguageResponse, GetLanguageResponse, CreateCountryResponse, GetCountryResponse, CreateSerieResponse, GetSeriesResponse, CreateCollectionResponse, GetCollectionResponse, CreatePublisherResponse, \
    GetPublisherResponse
from services.core import LanguageService, CountryService, SerieService, CollectionService, PublisherService

router = APIRouter(prefix='', tags=['Base'])


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


@router.post('/serie', status_code=status.HTTP_201_CREATED)
async def create_serie(serie: CreateSerieRequest,
                       session: AsyncSession = Depends(db_session)) -> CreateSerieResponse:
    response = await SerieService(session=session).create_serie(serie)

    return response


@router.get("/serie")
async def get_serie(session: AsyncSession = Depends(db_session)) -> GetSeriesResponse:
    response = await SerieService(session=session).get_series()

    return response


@router.post("/collection", status_code=status.HTTP_201_CREATED)
async def create_collection(collection: CreateCollectionRequest,
                            session: AsyncSession = Depends(db_session)) -> CreateCollectionResponse:
    response = await CollectionService(session=session).create_collection(collection)

    return response


@router.get("/collection")
async def get_collection(session: AsyncSession = Depends(db_session)) -> GetCollectionResponse:
    response = await CollectionService(session=session).get_collections()

    return response


@router.post('/publisher', status_code=status.HTTP_201_CREATED)
async def create_publisher(publisher: CreatePublisherRequest,
                           session: AsyncSession = Depends(db_session)) -> CreatePublisherResponse:
    response = await PublisherService(session).create_publisher(publisher)

    return response


@router.get('/publisher')
async def get_publisher(session: AsyncSession = Depends(db_session)) -> GetPublisherResponse:
    response = await PublisherService(session).get_publishers()

    return response
