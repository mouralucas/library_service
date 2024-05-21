import pytest
import pytest_asyncio
from fastapi import status

from managers.core import LanguageManager
from models import LanguageModel


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
    pass


@pytest.mark.asyncio
async def test_get_country(client):
    pass
