from typing import Any, cast

from rolf_common.managers import BaseDataManager
from sqlalchemy import RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    CollectionModel,
    CountryModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
    StatusModel,
)


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

    async def get_languages(self) -> list[dict[Any, Any]] | None:
        stmt = select(
            LanguageModel.id,
            LanguageModel.name,
            LanguageModel.code,
        )

        languages = await LanguageManager(session=self.session).get_all(
            select_statement=stmt
        )

        return [dict(language.items()) for language in languages] if languages else None


class CountryManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_country(self, country: CountryModel) -> CountryModel:
        """
        :Name: create_country
        :Created by: Lucas Penha de Moura - 21/05/2024
            Create a new country

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

    async def get_series(self) -> list[dict[Any, Any]] | None:
        query = select(
            SerieModel.id,
            SerieModel.name,
            SerieModel.original_name,
            SerieModel.description,
            SerieModel.country_id,
        )

        series = await self.get_all(query)

        return [dict(serie.items()) for serie in series] if series else None


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

    async def get_collections(self) -> list[dict[Any, Any]] | None:
        query = select(
            CollectionModel.id,
            CollectionModel.name,
            CollectionModel.description,
        )

        collections = await self.get_all(query)

        return (
            [dict(collection.items()) for collection in collections]
            if collections
            else None
        )


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

    async def get_publishers(self):
        query = (
            select(
                PublisherModel.id,
                PublisherModel.name,
                PublisherModel.description,
                PublisherModel.country_id,
                CountryModel.name.label("country_name"),
                PublisherModel.parent_id,
            )
            .select_from(PublisherModel)
            .outerjoin(CountryModel, PublisherModel.country_id == CountryModel.id)
        )

        publishers = await self.get_all(select_statement=query)

        return (
            [dict(publisher.items()) for publisher in publishers]
            if publishers
            else None
        )


class StatusManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_statuses(
        self, status_type: str | None = None
    ) -> list[dict[Any, Any]]:
        query = select(
            StatusModel.id,
            StatusModel.name,
            StatusModel.description,
            StatusModel.order,
            StatusModel.type.label("status_type"),
        ).where(StatusModel.active)

        if status_type:
            query = query.where(StatusModel.type == status_type)

        statuses: list[RowMapping] | None = await self.get_all(
            select_statement=query, unique_result=True
        )

        return [dict(status) for status in statuses] if statuses else []
