from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import BaseService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from managers.core import (
    CollectionManager,
    CountryManager,
    LanguageManager,
    PublisherManager,
    SerieManager,
    StatusManager,
)
from models import (
    CollectionModel,
    CountryModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
)
from schemas.core import (
    CollectionSchema,
    CountrySchema,
    LanguageSchema,
    PublisherSchema,
    SerieSchema,
    StatusSchema,
)
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


class LanguageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_language(
        self, language: CreateLanguageRequest
    ) -> CreateLanguageResponse:
        new_language = await LanguageManager(session=self.session).create_language(
            LanguageModel(**language.model_dump())
        )

        response = CreateLanguageResponse(
            language=LanguageSchema.model_validate(new_language)
        )

        return response

    async def get_languages(self) -> GetLanguageResponse:
        stmt = select(LanguageModel)

        languages = await LanguageManager(session=self.session).get_all(
            select_statement=stmt
        )

        response = GetLanguageResponse(
            quantity=len(languages) if languages else 0,
            languages=(
                [
                    LanguageSchema.model_validate(language["LanguageModel"])
                    for language in languages
                ]
                if languages
                else []
            ),
        )

        return response


class CountryService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(
        self, country: CreateCountryRequest
    ) -> CreateCountryResponse:
        new_country = await CountryManager(session=self.session).create_country(
            CountryModel(**country.model_dump())
        )

        response = CreateCountryResponse(
            country=CountrySchema.model_validate(new_country)
        )

        return response

    async def get_countries(self) -> GetCountryResponse:
        countries = await CountryManager(session=self.session).get_all(
            select_statement=select(CountryModel)
        )

        response = GetCountryResponse(
            quantity=len(countries) if countries else 0,
            countries=(
                [
                    CountrySchema.model_validate(country["CountryModel"])
                    for country in countries
                ]
                if countries
                else []
            ),
        )

        return response


class SerieService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_serie(self, serie: CreateSerieRequest) -> CreateSerieResponse:
        new_serie = await SerieManager(session=self.session).create_serie(
            SerieModel(**serie.model_dump())
        )

        response = CreateSerieResponse(serie=SerieSchema.model_validate(new_serie))

        return response

    async def get_series(self) -> GetSeriesResponse:
        # TODO:create manager, service should not contain db queries
        series = await SerieManager(session=self.session).get_all(select(SerieModel))

        response = GetSeriesResponse(
            quantity=len(series) if series else 0,
            series=(
                [SerieSchema.model_validate(serie["SerieModel"]) for serie in series]
                if series
                else []
            ),
        )

        return response


class CollectionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_collection(
        self, collection: CreateCollectionRequest
    ) -> CreateCollectionResponse:
        new_collection = await CollectionManager(
            session=self.session
        ).create_collection(CollectionModel(**collection.model_dump()))

        response = CreateCollectionResponse(
            collection=CollectionSchema.model_validate(new_collection)
        )

        return response

    async def get_collections(self) -> GetCollectionResponse:
        collections = await SerieManager(session=self.session).get_all(
            select(CollectionModel)
        )

        response = GetCollectionResponse(
            quantity=len(collections) if collections else 0,
            collections=(
                [
                    CollectionSchema.model_validate(collection["CollectionModel"])
                    for collection in collections
                ]
                if collections
                else []
            ),
        )

        return response


class PublisherService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_publisher(
        self, publisher: CreatePublisherRequest
    ) -> CreatePublisherResponse:
        new_publisher = await PublisherManager(session=self.session).create_publisher(
            PublisherModel(**publisher.model_dump())
        )

        response = CreatePublisherResponse(
            publisher=PublisherSchema.model_validate(new_publisher)
        )

        return response

    async def get_publishers(self) -> GetPublisherResponse:
        publishers = await PublisherManager(session=self.session).get_publishers()

        response = GetPublisherResponse(
            quantity=len(publishers) if publishers else 0,
            publishers=(
                [PublisherSchema.model_validate(publisher) for publisher in publishers]
                if publishers
                else []
            ),
        )

        return response


class StatusService(BaseService):
    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()

    async def get_status(self, params: GetStatusRequest) -> GetStatusResponse:
        statuses = await StatusManager(session=self.session).get_statuses(
            status_type=params.status_type
        )

        response = GetStatusResponse(
            quantity=len(statuses) if statuses else 0,
            statuses=(
                [StatusSchema.model_validate(s) for s in statuses] if statuses else []
            ),
        )

        return response
