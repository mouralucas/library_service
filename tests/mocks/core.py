import pytest_asyncio

from managers.author import AuthorManager
from rolf_common.managers import BaseDataManager
from managers.core import LanguageManager, CountryManager, SerieManager, CollectionManager, PublisherManager
from models import LanguageModel, CountryModel, SerieModel, CollectionModel, PublisherModel, AuthorModel, StatusModel


@pytest_asyncio.fixture
async def create_item_status(create_test_session):
    status_list = []

    status = StatusModel(id='owned', name='Na estante', type='ITEM.STATUS')
    status_1 = await BaseDataManager(session=create_test_session).add_one(status)

    status = StatusModel(id='bought', name='Comprado', type='ITEM.STATUS')
    status_2 = await BaseDataManager(session=create_test_session).add_one(status)

    status = StatusModel(id='desired', name='Desejado', type='ITEM.STATUS')
    status_3 = await BaseDataManager(session=create_test_session).add_one(status)

    status_list.append(status_1)
    status_list.append(status_2)
    status_list.append(status_3)

    return status_list


@pytest_asyncio.fixture
async def create_reading_status(create_test_session):
    reading_status_list = []

    status = StatusModel(id='reading', name='Lendo', type='READING.STATUS')
    status_1 = await BaseDataManager(session=create_test_session).add_one(status)

    status = StatusModel(id='read', name='Lido', type='READING.STATUS')
    status_2 = await BaseDataManager(session=create_test_session).add_one(status)

    reading_status_list.append(status_1)
    reading_status_list.append(status_2)

    return reading_status_list


@pytest_asyncio.fixture
async def create_languages(create_test_session):
    language_list = []

    language = LanguageModel(id='EN', name='English', code='EN')
    language_1 = await LanguageManager(session=create_test_session).create_language(language)

    language = LanguageModel(id='PT', name='Portuguese', code='PT')
    language_2 = await LanguageManager(session=create_test_session).create_language(language)

    language_list.append(language_1)
    language_list.append(language_2)

    return language_list


@pytest_asyncio.fixture
async def create_countries(create_test_session):
    countries_list = []

    country = CountryModel(id='BR', name='Brasil', continent='SA')
    country_1 = await CountryManager(session=create_test_session).create_country(country)

    country = CountryModel(id='DE', name='Alemanha', continent='EU')
    country_2 = await CountryManager(session=create_test_session).create_country(country)

    country = CountryModel(id='AU', name='Austrália', continent='OC')
    country_3 = await CountryManager(session=create_test_session).create_country(country)

    countries_list.append(country_1)
    countries_list.append(country_2)
    countries_list.append(country_3)

    return countries_list


@pytest_asyncio.fixture
async def create_series(create_test_session):
    series_list = []

    serie = SerieModel(id=0, name='Default', description='Default serie')
    serie_0 = await SerieManager(session=create_test_session).create_serie(serie)

    serie = SerieModel(name='Test serie', description='Test serie description')
    serie_1 = await SerieManager(session=create_test_session).create_serie(serie)

    serie = SerieModel(name='Test serie 2', description='Test serie 2 description')
    serie_2 = await SerieManager(session=create_test_session).create_serie(serie)

    series_list.append(serie_0)
    series_list.append(serie_1)
    series_list.append(serie_2)

    return series_list


@pytest_asyncio.fixture
async def create_collections(create_test_session) -> list:
    collections_list = []

    collection = CollectionModel(id=0, name='Default', description='Default collection')
    collection_0 = await CollectionManager(session=create_test_session).create_collection(collection)

    collection = CollectionModel(name='Test collection', description='Test collection description')
    collection_1 = await CollectionManager(session=create_test_session).create_collection(collection)

    collection = CollectionModel(name='Test collection 2', description='Test collection 2 description')
    collection_2 = await CollectionManager(session=create_test_session).create_collection(collection)

    collections_list.append(collection_0)
    collections_list.append(collection_1)
    collections_list.append(collection_2)

    return collections_list


@pytest_asyncio.fixture
async def create_publisher(create_test_session) -> list:
    publishers_list = []

    publisher = PublisherModel(name='Test publisher', description='Test publisher description')
    publisher_1 = await PublisherManager(session=create_test_session).create_publisher(publisher)

    publisher = PublisherModel(name='Other publisher', description='This is other publisher')
    publisher_2 = await PublisherManager(session=create_test_session).create_publisher(publisher)

    publishers_list.append(publisher_1)
    publishers_list.append(publisher_2)

    return publishers_list


@pytest_asyncio.fixture
async def create_authors(create_test_session,
                         create_languages,
                         create_countries) -> list:
    authors_list = []
    list_countries = create_countries
    list_languages = create_languages

    author = AuthorModel(name="Jack Ryan",
                         language_id=list_languages[0].id,
                         country_id=list_countries[0].id,
                         )
    author_1 = await AuthorManager(session=create_test_session).create_author(author)

    author = AuthorModel(name="Jason Bourne",
                         language_id=list_languages[1].id,
                         country_id=list_countries[1].id)
    author_2 = await AuthorManager(session=create_test_session).create_author(author)

    author = AuthorModel(name='Frodo Baggins',
                         language_id=list_languages[0].id,
                         country_id=list_countries[0].id)
    author_3 = await AuthorManager(session=create_test_session).create_author(author)

    authors_list.append(author_1)
    authors_list.append(author_2)
    authors_list.append(author_3)

    return authors_list
