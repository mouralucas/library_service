import pytest
import pytest_asyncio
from fastapi import status

from managers.core import LanguageManager, CountryManager
from models import LanguageModel, CountryModel


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


@pytest.mark.asyncio
async def test_create_language(client):
    language_id = 'EN'
    name = 'English'
    payload = {
        'id': language_id,
        'name': name,
        'code': language_id
    }

    response = await client.post("/core/language", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'language' in data
    assert data['language']['id'] == language_id
    assert data['language']['name'] == name
    assert data['language']['code'] == language_id


@pytest.mark.asyncio
async def test_get_language(client, create_languages):
    language_len = len(create_languages)

    response = await client.get("/core/language")

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'languages' in data
    assert type(data['languages']) is list
    assert len(data['languages']) == language_len


@pytest.mark.asyncio
async def test_create_country(client):
    country_id = 'BR'
    name = 'Brasil'
    continent = 'SA'

    payload = {
        'id': country_id,
        'name': name,
        'continent': continent
    }

    response = await client.post("/core/country", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'country' in data
    assert data['country']['id'] == country_id
    assert data['country']['name'] == name
    assert data['country']['continent'] == continent


@pytest.mark.asyncio
async def test_get_country(client, create_countries):
    country_len = len(create_countries)

    response = await client.get("/core/country")

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'countries' in data
    assert type(data['countries']) is list
    assert len(data['countries']) == country_len
