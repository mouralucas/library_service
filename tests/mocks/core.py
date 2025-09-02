import pytest_asyncio
from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel

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
from models import (
    AuthorModel,
    CollectionModel,
    CountryModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
    StatusModel,
)
from schemas.core import (
    AuthorSchema,
    CollectionSchema,
    CountrySchema,
    LanguageSchema,
    PublisherSchema,
    SerieSchema,
    StatusSchema,
)


@pytest_asyncio.fixture
async def create_item_status(create_test_session) -> list[StatusSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        StatusModel, get_item_status_mock()
    )
    item_status: list[StatusSchema] = (
        [StatusSchema.model_validate(data["StatusModel"]) for data in data_]
        if data_
        else []
    )

    return item_status


@pytest_asyncio.fixture
async def create_reading_status(create_test_session) -> list[StatusSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        StatusModel, get_reading_status_mock()
    )
    reading_status: list[StatusSchema] = (
        [StatusSchema.model_validate(data["StatusModel"]) for data in data_]
        if data_
        else []
    )

    return reading_status


@pytest_asyncio.fixture
async def create_languages(create_test_session) -> list[LanguageSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        LanguageModel, get_language_mock()
    )
    languages: list[LanguageSchema] = (
        [LanguageSchema.model_validate(data["LanguageModel"]) for data in data_]
        if data_
        else []
    )

    return languages


@pytest_asyncio.fixture
async def create_countries(create_test_session) -> list[CountrySchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        CountryModel, get_country_mock()
    )
    countries: list[CountrySchema] = (
        [CountrySchema.model_validate(data["CountryModel"]) for data in data_]
        if data_
        else []
    )

    return countries


@pytest_asyncio.fixture
async def create_series(create_test_session) -> list[SerieSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        SerieModel, get_serie_mock()
    )
    series: list[SerieSchema] = (
        [SerieSchema.model_validate(data["SerieModel"]) for data in data_]
        if data_
        else []
    )

    return series


@pytest_asyncio.fixture
async def create_collections(create_test_session) -> list[CollectionSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        CollectionModel, get_collection_mock()
    )
    collections: list[CollectionSchema] = (
        [CollectionSchema.model_validate(data["CollectionModel"]) for data in data_]
        if data_
        else []
    )

    return collections


@pytest_asyncio.fixture
async def create_publisher(create_test_session) -> list[PublisherSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        PublisherModel, get_publisher_mock()
    )
    publishers: list[PublisherSchema] = (
        [PublisherSchema.model_validate(data["PublisherModel"]) for data in data_]
        if data_
        else []
    )

    return publishers


@pytest_asyncio.fixture
async def create_authors(
    create_test_session, create_languages, create_countries
) -> list[AuthorSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        AuthorModel, get_author_mock()
    )
    authors: list[AuthorSchema] = (
        [AuthorSchema.model_validate(data["AuthorModel"]) for data in data_]
        if data_
        else []
    )

    return authors
