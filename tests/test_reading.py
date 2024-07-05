import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_reading(client, create_reading):
    param = {
        'itemId': create_reading[0].item_id,
        # 'itemId': 4,
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
async def test_create_reading(client, create_item, create_reading_status):
    items = create_item
    start_date = '2024-01-01'
    params = {
        "itemId": items[0].id,
        "startDate": start_date
    }
    response = await client.post("/reading", json=params)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data['success'] is True
    assert 'reading' in data

    assert 'readingId' in data['reading']
    assert data['reading']['readingId'] is not None
    # assert type(response_json['reading']['readingId']) is uuid.UUID

    assert 'itemId' in data['reading']
    assert data['reading']['itemId'] is not None
    assert data['reading']['itemId'] == items[0].id

    assert 'itemTitle' in data['reading']
    assert data['reading']['itemTitle'] is not None

    assert 'startDate' in data['reading']
    assert data['reading']['startDate'] is not None
    assert data['reading']['startDate'] == start_date

    assert 'readingNumber' in data['reading']
    assert data['reading']['readingNumber'] is not None
    assert data['reading']['readingNumber'] == 1

    assert 'progress' in data['reading']
    assert not data['reading']['progress']
    assert type(data['reading']['progress']) is list


@pytest.mark.asyncio
async def test_get_active_readings(client, create_reading):
    response = await client.get("/reading/active")

    total_readings = len(create_reading)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'quantity' in data
    assert data['quantity'] == total_readings

    assert 'readings' in data
    assert type(data['readings']) is list


@pytest.mark.asyncio
async def test_create_progress(client, create_reading):
    readings = create_reading

    reading_id = readings[0].id
    current_page = 37

    item = readings[0].item
    total_pages = item.pages
    percentage = int(current_page / total_pages * 100)

    payload = {
        'readingId': str(reading_id),
        'page': current_page
    }
    response = await client.post("/reading/progress", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data['success'] is True
    assert 'progress' in data
    assert 'page' in data['progress']
    assert 'percentage' in data['progress']
    assert data['progress']['page'] == current_page
    assert data['progress']['percentage'] == percentage


@pytest.mark.asyncio
async def test_get_progress(client, create_progress):
    progress = create_progress

    payload = {
        'readingId': progress[0].reading_id,
    }
    response = await client.get("/reading/progress", params=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'readingProgress' in data
    assert type(data['readingProgress']) is list
    # assert 'page' in data['progress']
    # assert 'percentage' in data['progress']
