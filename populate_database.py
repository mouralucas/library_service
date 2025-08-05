import asyncio

from rolf_common.managers import BaseDataManager

from backend.database import sessionmanager
from data_mock.core import (
    get_author_mock,
    get_collection_mock,
    get_country_mock,
    get_item_status_mock,
    get_language_mock,
    get_publisher_mock,
    get_reading_status_mock,
    get_serie_mock,
)
from data_mock.item import get_item_author_relation_mock, get_item_mock, get_item_status_relation_mock
from models import (
    AuthorModel,
    CollectionModel,
    CountryModel,
    ItemAuthorModel,
    ItemModel,
    ItemStatusModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
    StatusModel,
)


async def populate():
    async with sessionmanager.session() as session:
        await BaseDataManager(session).add_or_ignore_all(StatusModel, get_item_status_mock())
        await BaseDataManager(session).add_or_ignore_all(StatusModel, get_reading_status_mock())
        await BaseDataManager(session).add_or_ignore_all(LanguageModel, get_language_mock())
        await BaseDataManager(session).add_or_ignore_all(CountryModel, get_country_mock())
        await BaseDataManager(session).add_or_ignore_all(SerieModel, get_serie_mock())
        await BaseDataManager(session).add_or_ignore_all(CollectionModel, get_collection_mock())
        await BaseDataManager(session).add_or_ignore_all(PublisherModel, get_publisher_mock())
        await BaseDataManager(session).add_or_ignore_all(AuthorModel, get_author_mock())

        await BaseDataManager(session).add_or_ignore_all(ItemModel, get_item_mock())
        await BaseDataManager(session).add_or_ignore_all(ItemStatusModel, get_item_status_relation_mock())
        await BaseDataManager(session).add_or_ignore_all(ItemAuthorModel, get_item_author_relation_mock())


if __name__ == "__main__":
    asyncio.run(populate())
