import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

from managers.author import AuthorManager
from models import AuthorModel
from tests.test_misc import create_countries, create_languages


@pytest_asyncio.fixture
async def create_authors(create_test_session,
                         create_countries,
                         create_languages):
    authors_list = []
    list_countries = create_countries
    list_languages = create_languages

    author = AuthorModel(name="Autor da Silva",
                         language_id=list_languages[0].id,
                         country_id=list_countries[0].id,
                         )
    author_1 = await AuthorManager(session=create_test_session).create_author(author)

    author = AuthorModel(name="Autor de Souza",
                         language_id=list_languages[1].id,
                         country_id=list_countries[1].id)
    author_2 = await AuthorManager(session=create_test_session).create_author(author)

    authors_list.append(author_1)
    authors_list.append(author_2)

    return authors_list


@pytest.mark.asyncio
async def test_create_author(client):
    author_name = 'Test da Silva'
    payload = {
        'authorName': author_name,
    }
    response = await client.post('/author', json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert 'author' in data
    assert data['author']['authorName'] == author_name


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
