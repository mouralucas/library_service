import pytest
from fastapi import status


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
