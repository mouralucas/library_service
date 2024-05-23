import pytest_asyncio

from managers.core import LanguageManager, CountryManager, SerieManager, CollectionManager
from models import LanguageModel, CountryModel, SerieModel, CollectionModel


@pytest_asyncio.fixture
async def create_languages(create_test_session):
    language_list = []

    language = LanguageModel(id='PT', name='Portuguese', code='PT')
    language_1 = await LanguageManager(session=create_test_session).create_language(language)

    language = LanguageModel(id='EN', name='English', code='EN')
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

    serie = SerieModel(name='Test serie', description='Test serie description')
    serie_1 = await SerieManager(session=create_test_session).create_serie(serie)

    serie = SerieModel(name='Test serie 2', description='Test serie 2 description')
    serie_2 = await SerieManager(session=create_test_session).create_serie(serie)

    series_list.append(serie_1)
    series_list.append(serie_2)

    return series_list


@pytest_asyncio.fixture
async def create_collections(create_test_session) -> list:
    collections_list = []

    collection = CollectionModel(name='Test collection', description='Test collection description')
    collection_1 = await CollectionManager(session=create_test_session).create_collection(collection)

    collection = CollectionModel(name='Test collection 2', description='Test collection 2 description')
    collection_2 = await CollectionManager(session=create_test_session).create_collection(collection)

    collections_list.append(collection_1)
    collections_list.append(collection_2)

    return collections_list
