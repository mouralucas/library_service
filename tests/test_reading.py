import asyncio
import uuid

import pytest
import pytest_asyncio
from fastapi import status
from managers.base import BaseDataManager
from managers.item import ItemDataManager
from managers.reading import ReadingDataManager
from models import ReadingModel, ItemModel
import datetime
from main import app
from httpx import AsyncClient


@pytest_asyncio.fixture
async def create_item(create_test_session):
    item_list = []

    new_item = ItemModel(title="Test Item", owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"))
    item = await ItemDataManager(session=create_test_session).create_item(new_item)

    item_list.append(item)

    return item_list


@pytest_asyncio.fixture
async def create_reading(create_test_session, create_item):
    reading_list = []

    new_reading = ReadingModel(item_id=create_item[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"))
    await ReadingDataManager(session=create_test_session).create_reading(new_reading)

    reading_list.append(new_reading)

    return reading_list


@pytest.mark.asyncio
async def test_get_reading(create_reading):
    async with AsyncClient(app=app, base_url="http://test") as client:
        param = {
            'itemId': create_reading[0].item_id,
        }
        response = await client.get("/reading", params=param)

        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_json['success'] is True

        assert 'item_title' in response_json
        assert 'quantity' in response_json
        assert 'readings' in response_json

        # Check types from response
        assert type(response_json['quantity']) is int
        assert type(response_json['readings']) is list


@pytest.mark.asyncio
async def test_create_reading():
    async with AsyncClient(app=app, base_url="http://test") as client:
        item_id = 4  # create item
        start_date = '2024-01-01'
        params = {
            "itemId": item_id,
            "startDate": start_date
        }
        response = await client.post("/reading", json=params)

        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()

        assert response_json['success'] is True
        assert 'reading' in response_json

        assert 'readingId' in response_json['reading']
        assert response_json['reading']['readingId'] is not None
        # assert type(response_json['reading']['readingId']) is uuid.UUID

        assert 'itemId' in response_json['reading']
        assert response_json['reading']['itemId'] is not None
        assert response_json['reading']['itemId'] == item_id

        assert 'itemTitle' in response_json['reading']
        assert response_json['reading']['itemTitle'] is not None

        assert 'startDate' in response_json['reading']
        assert response_json['reading']['startDate'] is not None
        assert response_json['reading']['startDate'] == start_date

        assert 'readingNumber' in response_json['reading']
        assert response_json['reading']['readingNumber'] is not None
        assert response_json['reading']['readingNumber'] == 1

        assert 'progress' in response_json['reading']
        assert not response_json['reading']['progress']
        assert type(response_json['reading']['progress']) is list


@pytest.mark.asyncio
async def test_get_active_readings():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/reading/active")

    response_json = response.json()
    print(response_json)
