import pytest_asyncio
from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel

from data_mock.core import get_item_status_mocked, get_reading_status_mocked, get_language_mocked, get_country_mocked, get_serie_mocked, get_collection_mocked, get_publisher_mocked, get_author_mocked
from models import LanguageModel, CountryModel, SerieModel, CollectionModel, PublisherModel, AuthorModel, StatusModel
from schemas.core import StatusSchema, LanguageSchema, CountrySchema, SerieSchema, CollectionSchema, PublisherSchema, AuthorSchema


@pytest_asyncio.fixture
async def create_item_status(create_test_session) -> list[StatusSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(StatusModel, get_item_status_mocked())
    item_status: list[StatusSchema] = [StatusSchema.model_validate(data) for data in data_]

    return item_status


@pytest_asyncio.fixture
async def create_reading_status(create_test_session) -> list[StatusSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(StatusModel, get_reading_status_mocked())
    reading_status: list[StatusSchema] = [StatusSchema.model_validate(data) for data in data_]

    return reading_status


@pytest_asyncio.fixture
async def create_languages(create_test_session) -> list[LanguageSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(LanguageModel, get_language_mocked())
    languages: list[LanguageSchema] = [LanguageSchema.model_validate(data) for data in data_]

    return languages


@pytest_asyncio.fixture
async def create_countries(create_test_session) -> list[CountrySchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(CountryModel, get_country_mocked())
    countries: list[CountrySchema] = [CountrySchema.model_validate(data) for data in data_]

    return countries


@pytest_asyncio.fixture
async def create_series(create_test_session) -> list[SerieSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(SerieModel, get_serie_mocked())
    series: list[SerieSchema] = [SerieSchema.model_validate(data) for data in data_]

    return series


@pytest_asyncio.fixture
async def create_collections(create_test_session) -> list[CollectionSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(CollectionModel, get_collection_mocked())
    collections: list[CollectionSchema] = [CollectionSchema.model_validate(data) for data in data_]

    return collections


@pytest_asyncio.fixture
async def create_publisher(create_test_session) -> list[PublisherSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(PublisherModel, get_publisher_mocked())
    publishers: list[PublisherSchema] = [PublisherSchema.model_validate(data) for data in data_]

    return publishers


@pytest_asyncio.fixture
async def create_authors(create_test_session, create_languages, create_countries) -> list[AuthorSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(AuthorModel, get_author_mocked())
    authors: list[AuthorSchema] = [AuthorSchema.model_validate(data) for data in data_]

    return authors