from typing import Any

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
    GetCountryResponse,
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

    async def get_languages(self) -> dict[str, Any]:

        languages = await LanguageManager(session=self.session).get_languages()

        response = {
            "quantity": len(languages) if languages else 0,
            "languages": languages,
        }

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

    async def get_series(self) -> dict[str, Any]:
        series = await SerieManager(session=self.session).get_series()

        response = {"quantity": len(series) if series else 0, "series": series}

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

    async def get_collections(self) -> dict[str, Any]:
        collections = await CollectionManager(session=self.session).get_collections()

        response = {
            "quantity": len(collections) if collections else 0,
            "collections": collections,
        }

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

    async def get_publishers(self) -> dict[str, Any]:
        publishers = await PublisherManager(session=self.session).get_publishers()

        response = {
            "quantity": len(publishers) if publishers else 0,
            "publishers": publishers,
        }

        return response


class StatusService(BaseService):
    def __init__(self, session: AsyncSession, user: RequiredUser):
        super().__init__(session)
        self.user = user.model_dump()

    async def get_status(self, params: GetStatusRequest) -> dict[str, Any]:
        statuses = await StatusManager(session=self.session).get_statuses(
            status_type=params.status_type
        )

        response = {"quantity": len(statuses) if statuses else 0, "statuses": statuses}

        return response
