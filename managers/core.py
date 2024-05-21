from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models import LanguageModel, SQLModel, CountryModel


class LanguageManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_language(self, language: LanguageModel) -> SQLModel:
        """
        :Name: create_language
        :Created by: Lucas Penha de Moura - 20/05/2024
            Create a new language

            Params:
                language: an instance of LanguageModel
        """
        new_language = await self.add_one(language)

        return new_language


class CountryManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(self, country: CountryModel) -> SQLModel:
        """
        :Name: create_country
        :Created by: Lucas Penha de Moura - 21/05/2024
            Create a new language

            Params:
                language: an instance of CountryModel
        """
        new_country = await self.add_one(country)

        return new_country
