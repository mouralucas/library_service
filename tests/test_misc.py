import pytest
import pytest_asyncio
from fastapi import status

from managers.core import LanguageManager, CountryManager
from models import LanguageModel, CountryModel
from tests.mocks.core import create_collections, create_series, create_countries, create_languages


@pytest.mark.asyncio
async def test_create_language(client):
    language_id = 'EN'
    name = 'English'
    payload = {
        'id': language_id,
        'name': name,
        'code': language_id
    }

    response = await client.post("/language", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'language' in data
    assert data['language']['id'] == language_id
    assert data['language']['name'] == name
    assert data['language']['code'] == language_id


@pytest.mark.asyncio
async def test_get_language(client, create_languages):
    language_len = len(create_languages)

    response = await client.get("/language")

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

    response = await client.post("/country", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'country' in data
    assert data['country']['id'] == country_id
    assert data['country']['name'] == name
    assert data['country']['continent'] == continent


@pytest.mark.asyncio
async def test_get_country(client, create_countries):
    country_len = len(create_countries)

    response = await client.get("/country")

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'countries' in data
    assert type(data['countries']) is list
    assert len(data['countries']) == country_len


@pytest.mark.asyncio
async def test_create_serie(client):
    serie_name = 'Serie Test'

    payload = {
        'serieName': serie_name
    }
    response = await client.post('/serie', json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'serie' in data
    assert data['serie']['serieName'] == serie_name


@pytest.mark.asyncio
async def test_get_serie(client, create_series):
    series = create_series
    series_list_len = len(series)

    response = await client.get('/serie')

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'series' in data
    assert type(data['series']) is list
    assert len(data['series']) == series_list_len
    assert data['series'][0]['serieName'] == series[0].name


@pytest.mark.asyncio
async def test_create_collection(client):
    collection_name = 'Test Collection'
    collections_description = 'Test description'

    payload = {
        'collectionName': collection_name,
        'description': collections_description
    }
    response = await client.post('/collection', json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'collection' in data
    assert data['collection']['collectionName'] == collection_name
    assert data['collection']['description'] == collections_description


@pytest.mark.asyncio
async def test_get_collection(client, create_collections):
    collections = create_collections
    collections_list_len = len(collections)

    response = await client.get('/collection')

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'collections' in data
    assert type(data['collections']) is list
    assert len(data['collections']) == collections_list_len
    assert data['collections'][0]['collectionName'] == collections[0].name


@pytest.mark.asyncio
async def test_create_publisher(client):
    publisher_name = 'Test Publisher'
    description = 'Test description'

    payload = {
        'publisherName': publisher_name,
        'description': description
    }
    response = await client.post('/publisher', json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert 'publisher' in data
    assert data['publisher']['publisherName'] == publisher_name
    assert data['publisher']['description'] == description
