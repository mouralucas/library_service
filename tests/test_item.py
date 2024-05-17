import pytest
from httpx import AsyncClient
from fastapi import status

from main import app


async def test_create_item_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post('/item', json={'name': 'test'})

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_item():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/item')

        assert response.status_code == status.HTTP_200_OK
