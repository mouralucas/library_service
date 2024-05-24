import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_author_fail(client):
    response = await client.post("/author")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_author_with_name_only(client):
    author_name = 'Test da Silva'

    payload = {
        'authorName': author_name,
    }
    response = await client.post('/author', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert 'author' in data
    assert data['author']['authorName'] == author_name

    assert 'countryId' in data['author']
    assert data['author']['countryId'] is None

    assert 'languageId' in data['author']
    assert data['author']['languageId'] is None


@pytest.mark.asyncio
async def test_create_author_success(client, create_languages, create_countries):
    author_name = 'Test da Silva'
    languages = create_languages
    countries = create_countries

    payload = {
        'authorName': author_name,
        'languageId': languages[0].id,
        'countryId': countries[0].id,
    }
    response = await client.post('/author', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert 'author' in data
    assert data['author']['authorName'] == author_name

    assert 'countryId' in data['author']
    assert data['author']['countryId'] == countries[0].id

    assert 'languageId' in data['author']
    assert data['author']['languageId'] == languages[0].id


@pytest.mark.asyncio
async def test_create_author_fail(client):
    response = await client.post("/author")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()

    assert 'detail' in data


@pytest.mark.asyncio
async def test_get_author(client, create_authors):
    response = await client.get('/author')
    len_authors_list = len(create_authors)

    data = response.json()
    assert response.status_code == status.HTTP_200_OK

    assert 'authors' in data
    assert len(data['authors']) == len_authors_list
    assert type(data['authors']) is list
    assert data['quantity'] == len_authors_list
