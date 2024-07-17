import pytest
from fastapi import status


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
async def test_get_reading_by_item_id(client, create_more_than_one_reading):
    readings = create_more_than_one_reading

    reading_id = readings[0].id
    item_id = readings[0].item_id

    param = {
        'itemId': item_id,
    }
    response = await client.get("/reading", params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'item_title' in data
    assert 'quantity' in data
    assert 'readings' in data

    # Check types from response
    assert type(data['quantity']) is int
    assert type(data['readings']) is list

    assert data['quantity'] > 1
    assert len(data['readings']) > 0

    assert 'readingId' in data['readings'][0]
    assert data['readings'][0]['readingId'] == str(reading_id)

    assert 'itemId' in data['readings'][0]
    assert data['readings'][0]['itemId'] == item_id


@pytest.mark.asyncio
async def test_get_reading_by_reading_id(client, create_more_than_one_reading):
    """
        Exacly the same as test_get_reading_by_item_id, but in this case reading_id is used to get a reading. It must return only one instance
    :param client:
    :param create_reading:
    :return:
    """
    readings = create_more_than_one_reading

    reading_id = readings[0].id
    item_id = readings[0].item_id

    param = {
        'readingId': reading_id,
    }
    response = await client.get("/reading", params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'item_title' in data
    assert 'quantity' in data
    assert 'readings' in data

    # Check types from response
    assert type(data['quantity']) is int
    assert type(data['readings']) is list

    assert data['quantity'] == 1
    assert len(data['readings']) > 0
    assert 'readingId' in data['readings'][0]
    assert data['readings'][0]['readingId'] == str(reading_id)

    assert 'itemId' in data['readings'][0]
    assert data['readings'][0]['itemId'] == item_id


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
async def test_create_progress_with_page(client, create_reading):
    readings = create_reading

    reading_id = readings[0].id
    current_page = 42

    item = readings[0].item
    total_pages = item.pages
    percentage = float(current_page / total_pages * 100)

    payload = {
        'readingId': str(reading_id),
        'page': current_page
    }
    response = await client.post("/reading/progress", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert 'progress' in data
    assert 'page' in data['progress']
    assert 'percentage' in data['progress']
    assert data['progress']['page'] == current_page
    assert data['progress']['percentage'] == percentage


@pytest.mark.asyncio
async def test_create_progress_with_percentage(client, create_reading):
    readings = create_reading

    reading_id = readings[0].id
    current_percentage = 32

    item = readings[0].item
    total_pages = item.pages
    page = int(current_percentage / 100 * total_pages)

    payload = {
        'readingId': str(reading_id),
        'percentage': current_percentage
    }
    response = await client.post("/reading/progress", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert 'progress' in data
    assert 'page' in data['progress']
    assert 'percentage' in data['progress']
    assert data['progress']['page'] == page
    assert data['progress']['percentage'] == current_percentage


@pytest.mark.asyncio
async def test_create_progress_fail(client, create_reading):
    readings = create_reading

    reading_id = readings[0].id
    item = readings[0].item

    # Set page greater than the item
    current_page = item.pages + 5
    payload = {
        'readingId': str(reading_id),
        'page': current_page
    }
    response = await client.post("/reading/progress", json=payload)

    assert response.status_code == status.HTTP_428_PRECONDITION_REQUIRED


@pytest.mark.asyncio
async def test_create_progress_complete_reading(client, create_reading):
    reading = create_reading

    current_reading = reading[0]
    reading_id = current_reading.id
    current_percentage = 100

    payload = {
        'readingId': str(reading_id),
        'percentage': current_percentage
    }
    response = await client.post('/reading/progress', json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    # TODO: after create a get_reading by reading id, add the request and check with the request not the referenced object
    assert current_reading.active is False
    assert current_reading.status_id == 'read'


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
