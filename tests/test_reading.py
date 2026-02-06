import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_reading(client, create_item, create_reading_status):
    items = create_item
    start_date = "2024-01-01"
    params = {"itemId": items[0].id, "startDate": start_date}
    response = await client.post("/reading", json=params)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "created" in data
    assert data["created"] is True
    assert "readingId" in data


@pytest.mark.asyncio
async def test_create_finished_reading(client, create_item, create_reading_status):
    pass


@pytest.mark.asyncio
async def test_create_reading_without_start_date(
    client, create_item, create_reading_status
):
    """
    This test is to check if the start_date is set to current date when not provided
    So the validation here is just to check if the response has a 'reading' key
    """
    items = create_item

    params = {
        "itemId": items[0].id,
    }
    response = await client.post("/reading", json=params)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert "created" in data
    assert data["created"] is True
    assert "readingId" in data


@pytest.mark.asyncio
async def test_get_reading_by_item_id(client, create_more_than_one_reading):
    readings = create_more_than_one_reading

    item_id = readings[0].item_id

    param = {
        "itemId": item_id,
    }
    query = """
        query GetReadings($params: GetReadingsInput) {
            getReadings(params: $params) {
                quantity
                readings {
                    id
                    itemId
                    itemTitle
                    startDate
                    finishDate
                    number
                    active
                    statusId
                    statusName
                }
            }
        }
    """
    variables = {"params": param}
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "getReadings" in data["data"]
    assert "quantity" in data["data"]["getReadings"]
    assert "readings" in data["data"]["getReadings"]

    data = data["data"]["getReadings"]
    assert "quantity" in data
    assert "readings" in data

    # Check types from response
    assert type(data["quantity"]) is int
    assert type(data["readings"]) is list

    assert data["quantity"] > 1
    assert len(data["readings"]) > 0

    for reading in data["readings"]:
        assert "id" in reading
        assert "itemId" in reading
        assert reading["itemId"] == item_id


@pytest.mark.asyncio
async def test_get_reading_by_reading_id(client, create_more_than_one_reading):
    """
        Exactly the same as test_get_reading_by_item_id,
            but in this case reading_id is used to get a reading.
        It must return only one instance
    :param client:
    :param create_reading:
    :return:
    """
    readings = create_more_than_one_reading

    reading_id = readings[0].id
    item_id = readings[0].item_id

    param = {
        "readingId": str(reading_id),
    }
    query = """
        query GetReadings($params: GetReadingsInput) {
            getReadings(params: $params) {
                quantity
                readings {
                    id
                    itemId
                    itemTitle
                    startDate
                    finishDate
                    number
                    active
                    statusId
                    statusName
                }
            }
        }
    """
    variables = {"params": param}
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "getReadings" in data["data"]
    assert "quantity" in data["data"]["getReadings"]
    assert "readings" in data["data"]["getReadings"]

    data = data["data"]["getReadings"]
    assert "quantity" in data
    assert "readings" in data

    # Check types from response
    assert type(data["quantity"]) is int
    assert type(data["readings"]) is list

    # When filter by reading Id only one have to be returned
    assert data["quantity"] == 1
    assert len(data["readings"]) == 1

    for reading in data["readings"]:
        assert "id" in reading
        assert "itemId" in reading
        assert reading["itemId"] == item_id
        assert "id" in reading
        assert reading["id"] == str(reading_id)

        assert "itemId" in reading
        assert reading["itemId"] == item_id


@pytest.mark.asyncio
async def test_get_active_readings(client, create_active_active_readings):
    response = await client.get("/reading/active")

    total_readings = len(create_active_active_readings)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "quantity" in data
    assert data["quantity"] == total_readings

    assert "readings" in data
    assert type(data["readings"]) is list


@pytest.mark.asyncio
async def test_create_progress_with_page(client, create_active_active_readings):
    reading = create_active_active_readings[0]

    reading_id = reading.id
    current_page = 42

    item = reading.item
    item_title = item.title
    progress_type = "page"

    payload = {
        "readingId": str(reading_id),
        "progressType": progress_type,
        "value": current_page,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createReadingProgress" in data["data"]

    data = data["data"]["createReadingProgress"]
    assert "created" in data
    assert data["created"] is True

    assert "readingProgressId" in data
    assert "itemTitle" in data
    assert data["itemTitle"] == item_title


@pytest.mark.asyncio
async def test_create_progress_with_percentage(client, create_active_active_readings):
    reading = create_active_active_readings[0]

    reading_id = reading.id
    current_percentage = 32

    item = reading.item
    item_title = item.title
    progress_type = "percentage"

    payload = {
        "readingId": str(reading_id),
        "progressType": progress_type,
        "value": current_percentage,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createReadingProgress" in data["data"]

    data = data["data"]["createReadingProgress"]
    assert "created" in data
    assert data["created"] is True

    assert "readingProgressId" in data
    assert "itemTitle" in data
    assert data["itemTitle"] == item_title


@pytest.mark.asyncio
async def test_create_progress_lt_last_progress(client, create_progress):
    progress = create_progress

    reading_id = progress[0].reading_id
    last_progress_page = progress[-1].page
    last_progress_percentage = progress[-1].percentage
    current_progress_page = last_progress_page - 5
    current_progress_percentage = last_progress_percentage - 3

    # test with page
    payload = {
        "readingId": str(reading_id),
        "progressType": "page",
        "value": current_progress_page,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # TODO: graphql returns 200 even when an error is thrown
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "errors" in data

    # test with percentage
    payload = {
        "readingId": str(reading_id),
        "progressType": "percentage",
        "value": current_progress_percentage,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # TODO: graphql returns 200 even when an error is thrown
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "errors" in data


@pytest.mark.asyncio
async def test_create_progress_percentage_gt_100(client, create_active_active_readings):
    reading = create_active_active_readings[0]

    reading_id = reading.id
    item = reading.item

    # Set page greater than the item
    current_page = item.pages + 5
    payload = {
        "readingId": str(reading_id),
        "progressType": "page",
        "value": current_page,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # TODO: graphql returns 200 even when an error is thrown
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "errors" in data

    # Test with more than 100%
    payload = {"readingId": str(reading_id), "progressType": "percentage", "value": 105}
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # TODO: graphql returns 200 even when an error is thrown
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "errors" in data


@pytest.mark.asyncio
async def test_create_progress_complete_reading_pages(
    client, create_active_active_readings
):
    reading = create_active_active_readings[0]

    current_reading = reading
    reading_id = current_reading.id
    item = reading.item
    item_pages = item.pages
    current_page = item_pages

    payload = {
        "readingId": str(reading_id),
        "progressType": "page",
        "value": current_page,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                created
                readingProgressId
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createReadingProgress" in data["data"]

    data = data["data"]["createReadingProgress"]

    payload = {
        "readingId": str(reading_id),
    }
    query = """
        query GetReadings($params: GetReadingsInput) {
            getReadings(params: $params) {
                quantity
                readings {
                    id
                    itemId
                    itemTitle
                    startDate
                    finishDate
                    number
                    active
                    statusId
                    statusName
                }
            }
        }
    """
    variables = {"params": payload}
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    data = response.json()
    assert "data" in data
    assert "getReadings" in data["data"]
    assert "quantity" in data["data"]["getReadings"]
    assert "readings" in data["data"]["getReadings"]

    data = data["data"]["getReadings"]

    updated_reading = data["readings"][0]

    assert updated_reading["active"] is False
    assert updated_reading["statusId"] == "read"
    assert updated_reading["statusName"] == "Lido"
    assert updated_reading["finishDate"] is not None


@pytest.mark.asyncio
async def test_create_progress_complete_reading_percentage(
    client, create_active_active_readings
):
    reading = create_active_active_readings[0]

    current_reading = reading
    reading_id = current_reading.id
    current_percentage = 100

    payload = {
        "readingId": str(reading_id),
        "progressType": "percentage",
        "value": current_percentage,
    }
    mutation = """
        mutation CreateReadingProgress($progress: CreateReadingProgressInput!) {
            createReadingProgress(progress: $progress) {
                itemTitle
                itemTitle
                created
            }
        }
    """
    variables = {"progress": payload}
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createReadingProgress" in data["data"]

    payload = {
        "readingId": str(reading_id),
    }
    query = """
        query GetReadings($params: GetReadingsInput) {
            getReadings(params: $params) {
                quantity
                readings {
                    id
                    itemId
                    itemTitle
                    startDate
                    finishDate
                    number
                    active
                    statusId
                    statusName
                }
            }
        }
    """
    variables = {"params": payload}
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    data = response.json()
    assert "data" in data
    assert "getReadings" in data["data"]
    assert "quantity" in data["data"]["getReadings"]
    assert "readings" in data["data"]["getReadings"]

    data = data["data"]["getReadings"]

    updated_reading = data["readings"][0]

    assert updated_reading["active"] is False
    assert updated_reading["statusId"] == "read"
    assert updated_reading["statusName"] == "Lido"
    assert updated_reading["finishDate"] is not None


@pytest.mark.asyncio
async def test_get_progress(client, create_progress):
    progress = create_progress

    payload = {
        "readingId": progress[0].reading_id,
    }
    response = await client.get("/reading/progress", params=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "readingProgress" in data
    assert type(data["readingProgress"]) is list
    # assert 'page' in data['progress']
    # assert 'percentage' in data['progress']


@pytest.mark.asyncio
async def test_get_reading_stats_no_reading_for_item(client, create_item):
    item = create_item[0]
    item_id = item.id

    payload = {
        "itemId": item_id,
    }
    response = await client.get("/reading/stats", params=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "stats" in data
    assert "readingsCount" in data["stats"]
    assert data["stats"]["readingsCount"] == 0
    assert "lastReadingDate" in data["stats"]
    assert data["stats"]["lastReadingDate"] is None
    # assert 'averageReadingTime' in data['stats']
    # assert data['stats']['averageReadingTime'] is None
    assert "currentPage" in data["stats"]
    assert data["stats"]["currentPage"] is None
    assert "currentPercentage" in data["stats"]
    assert data["stats"]["currentPercentage"] is None
