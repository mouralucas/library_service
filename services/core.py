from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.core import LanguageManager, CountryManager
from models import LanguageModel, CountryModel
from schemas.core import LanguageSchema, CountrySchema
from schemas.request.core import CreateLanguageRequest, CreateCountryRequest
from schemas.response.core import CreateLanguageResponse, GetLanguageResponse, CreateCountryResponse, GetCountryResponse
from services.base import BaseService


class LanguageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_language(self, language: CreateLanguageRequest) -> CreateLanguageResponse:
        new_language = await LanguageManager(session=self.session).create_language(LanguageModel(**language.dict()))

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
            languages=[LanguageSchema.model_validate(language) for language in languages] if languages else []
        )

        return response


class CountryService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(self, country: CreateCountryRequest) -> CreateCountryResponse:
        new_country = await CountryManager(session=self.session).create_country(CountryModel(**country.dict()))

        response = CreateCountryResponse(
            status_code=status.HTTP_201_CREATED,
            country=CountrySchema.model_validate(new_country)
        )

        return response

    async def get_countries(self) -> GetCountryResponse:
        countries = await CountryManager(session=self.session).get_all(select_stmt=select(CountryModel))

        response = GetCountryResponse(
            status_code=status.HTTP_200_OK,
            countries=[CountrySchema.model_validate(country) for country in countries] if countries else []
        )

        return response
