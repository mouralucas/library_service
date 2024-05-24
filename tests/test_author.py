import pytest
from fastapi import status

from tests.mocks.core import create_authors, create_countries


@pytest.mark.asyncio
async def test_create_author_fail(client):
    response = await client.post("/author")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


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
