from typing import cast

from rolf_common.managers import BaseDataManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import LanguageModel, SQLModel, CountryModel, CollectionModel, SerieModel, PublisherModel, StatusModel


class LanguageManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_language(self, language: LanguageModel) -> LanguageModel:
        """
        :Name: create_language
        :Created by: Lucas Penha de Moura - 20/05/2024
            Create a new language

        :Params:
            language: an instance of LanguageModel
        """
        new_language = await self.add_one(language)

        return cast(LanguageModel, new_language)


class CountryManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(self, country: CountryModel) -> CountryModel:
        """
        :Name: create_country
        :Created by: Lucas Penha de Moura - 21/05/2024
            Create a new language

        :Params:
            country: an instance of CountryModel
        """
        new_country = await self.add_one(country)

        return cast(CountryModel, new_country)


class SerieManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_serie(self, serie: SerieModel) -> SerieModel:
        """
        :Name: create_country
        :Created by: Lucas Penha de Moura - 22/05/2024
            Create a new serie

        :Params:
            serie: an instance of SerieModel
        """
        new_serie = await self.add_one(serie)

        return cast(SerieModel, new_serie)


class CollectionManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_collection(self, collection: CollectionModel) -> CollectionModel:
        """
        :Name: create_collection
        :Created by: Lucas Penha de Moura - 22/05/2024
            Create a new collection

        :Params:
            collection: an instance of CollectionModel
        """
        new_collection = await self.add_one(collection)

        return cast(CollectionModel, new_collection)


class PublisherManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_publisher(self, publisher: PublisherModel) -> PublisherModel:
        """
        :Name: create_publisher
        :Created by: Lucas Penha de Moura - 23/05/2024
            Create a new publisher

        :Params:
            publisher: an instance of PublisherModel
        """
        new_publisher = await self.add_one(publisher)

        return cast(PublisherModel, new_publisher)


class StatusManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_status(self, status_type: str) -> StatusModel:
        stmt = select(StatusModel).where(StatusModel.type == status_type)

        status: SQLModel = await self.get_only_one(stmt)

        return cast(StatusModel, status)
