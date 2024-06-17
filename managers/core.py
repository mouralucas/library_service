from sqlalchemy.ext.asyncio import AsyncSession

from rolf_common.managers import BaseDataManager
from models import LanguageModel, SQLModel, CountryModel, CollectionModel, SerieModel, PublisherModel


class LanguageManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_language(self, language: LanguageModel) -> SQLModel:
        """
        :Name: create_language
        :Created by: Lucas Penha de Moura - 20/05/2024
            Create a new language

        :Params:
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

        :Params:
            country: an instance of CountryModel
        """
        new_country = await self.add_one(country)

        return new_country


class SerieManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_serie(self, serie: SerieModel) -> SQLModel:
        """
        :Name: create_country
        :Created by: Lucas Penha de Moura - 22/05/2024
            Create a new serie

        :Params:
            serie: an instance of SerieModel
        """
        new_serie = await self.add_one(serie)

        return new_serie


class CollectionManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_collection(self, collection: CollectionModel) -> SQLModel:
        """
        :Name: create_collection
        :Created by: Lucas Penha de Moura - 22/05/2024
            Create a new collection

        :Params:
            collection: an instance of CollectionModel
        """
        new_collection = await self.add_one(collection)

        return new_collection


class PublisherManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_publisher(self, publisher: PublisherModel) -> SQLModel:
        """
        :Name: create_publisher
        :Created by: Lucas Penha de Moura - 23/05/2024
            Create a new publisher

        :Params:
            publisher: an instance of PublisherModel
        """
        new_publisher = await self.add_one(publisher)

        return new_publisher
