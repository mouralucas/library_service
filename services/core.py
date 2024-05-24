from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.core import LanguageManager, CountryManager, SerieManager, CollectionManager, PublisherManager
from models import LanguageModel, CountryModel, SerieModel, CollectionModel, PublisherModel
from schemas.core import LanguageSchema, CountrySchema, SerieSchema, CollectionSchema, PublisherSchema
from schemas.request.core import CreateLanguageRequest, CreateCountryRequest, CreateSerieRequest, CreateCollectionRequest, CreatePublisherRequest
from schemas.response.core import CreateLanguageResponse, GetLanguageResponse, CreateCountryResponse, GetCountryResponse, CreateSerieResponse, GetSeriesResponse, GetCollectionResponse, CreateCollectionResponse, CreatePublisherResponse, \
    GetPublisherResponse
from services.base import BaseService


class LanguageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_language(self, language: CreateLanguageRequest) -> CreateLanguageResponse:
        new_language = await LanguageManager(session=self.session).create_language(LanguageModel(**language.model_dump()))

        response = CreateLanguageResponse(
            status_code=status.HTTP_201_CREATED,
            language=LanguageSchema.model_validate(new_language)
        )

        return response

    async def get_languages(self) -> GetLanguageResponse:
        stmt = select(LanguageModel)

        languages = await LanguageManager(session=self.session).get_all(select_stmt=stmt)

        response = GetLanguageResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(languages) if languages else 0,
            languages=[LanguageSchema.model_validate(language) for language in languages] if languages else []
        )

        return response


class CountryService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(self, country: CreateCountryRequest) -> CreateCountryResponse:
        new_country = await CountryManager(session=self.session).create_country(CountryModel(**country.model_dump()))

        response = CreateCountryResponse(
            status_code=status.HTTP_201_CREATED,
            country=CountrySchema.model_validate(new_country)
        )

        return response

    async def get_countries(self) -> GetCountryResponse:
        countries = await CountryManager(session=self.session).get_all(select_stmt=select(CountryModel))

        response = GetCountryResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(countries) if countries else 0,
            countries=[CountrySchema.model_validate(country) for country in countries] if countries else []
        )

        return response


class SerieService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_serie(self, serie: CreateSerieRequest) -> CreateSerieResponse:
        new_serie = await SerieManager(session=self.session).create_serie(SerieModel(**serie.model_dump()))

        response = CreateSerieResponse(
            status_code=status.HTTP_201_CREATED,
            serie=SerieSchema.model_validate(new_serie)
        )

        return response

    async def get_series(self) -> GetSeriesResponse:
        series = await SerieManager(session=self.session).get_all(select(SerieModel))

        response = GetSeriesResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(series) if series else 0,
            series=[SerieSchema.model_validate(serie) for serie in series] if series else []
        )

        return response


class CollectionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_collection(self, collection: CreateCollectionRequest) -> CreateCollectionResponse:
        new_collection = await CollectionManager(session=self.session).create_collection(CollectionModel(**collection.model_dump()))

        response = CreateCollectionResponse(
            status_code=status.HTTP_201_CREATED,
            collection=CollectionSchema.model_validate(new_collection)
        )

        return response

    async def get_collections(self) -> GetCollectionResponse:
        collections = await SerieManager(session=self.session).get_all(select(CollectionModel))

        response = GetCollectionResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(collections) if collections else 0,
            collections=[CollectionSchema.model_validate(collection) for collection in collections] if collections else []
        )

        return response


class PublisherService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_publisher(self, publisher: CreatePublisherRequest) -> CreatePublisherResponse:
        new_publisher = await PublisherManager(session=self.session).create_publisher(PublisherModel(**publisher.model_dump()))

        response = CreatePublisherResponse(
            status_code=status.HTTP_201_CREATED,
            publisher=PublisherSchema.model_validate(new_publisher)
        )

        return response

    async def get_publishers(self) -> GetPublisherResponse:
        publishers = await PublisherManager(session=self.session).get_all(select(PublisherModel))

        response = GetPublisherResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(publishers) if publishers else 0,
            publishers=[PublisherSchema.model_validate(publisher) for publisher in publishers] if publishers else []
        )

        return response
