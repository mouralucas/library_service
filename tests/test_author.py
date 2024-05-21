import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_author(client):
    response = await client.get('/author')

    assert response.status_code == status.HTTP_200_OK
