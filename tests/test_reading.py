from datetime import date

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
        "progressDate": date.today().strftime("%Y-%m-%d"),
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
        "progressDate": date.today().strftime("%Y-%m-%d"),
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
        "progressDate": date.today().strftime("%Y-%m-%d"),
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
        "progressDate": date.today().strftime("%Y-%m-%d"),
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
        "progressDate": date.today().strftime("%Y-%m-%d"),
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
async def test_create_progress_complete_reading_percentage_with_goal(
    client, create_active_active_readings
):
    reading = create_active_active_readings[0]

    current_reading = reading
    reading_id = current_reading.id
    current_percentage = 100

    payload = {
        "readingId": str(reading_id),
        "progressType": "percentage",
        "progressDate": date.today().strftime("%Y-%m-%d"),
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


@pytest.mark.asyncio
async def test_get_progress(client, create_progress):
    progress = create_progress

    payload = {
        "readingId": str(progress[0].reading_id),
    }
    query = """
        query GetReadingProgress($params: GetReadingProgressInput) {
            getReadingProgress(params: $params ) {
                quantity
                itemTitle
                pagesRead
                progress {
                    id
                    progressDate
                    page
                    percentage
                    rate
                    comment
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
    assert "data" in data
    assert "getReadingProgress" in data["data"]

    data = data["data"]["getReadingProgress"]

    assert "progress" in data
    assert type(data["progress"]) is list


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


# Tests for Reading Queue Logic
@pytest.mark.asyncio
async def test_create_reading_adds_item_to_queue_if_not_present(
    client, create_item, create_reading_status, create_test_session
):
    """
    Test that when a reading is created for an item not in the queue,
    the item is automatically added to the reading queue for the current year.
    """
    import uuid as uuid_module

    from managers.reading import ReadingManager

    item = create_item[0]
    start_date = date.today()

    # Create a reading
    params = {
        "itemId": item.id,
        "startDate": start_date.strftime("%Y-%m-%d"),
    }
    response = await client.post("/reading", json=params)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["created"] is True

    # Verify that an item queue entry was created by checking the database directly
    user_id = uuid_module.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002")
    user_dict = {"user_id": user_id}
    reading_manager = ReadingManager(session=create_test_session, user=user_dict)

    # Check if goal was created for this item in the current year
    goal = await reading_manager.get_active_goal_by_item_id(item_id=item.id)
    assert goal is not None, "Item should be added to reading queue"
    assert goal.year == start_date.year, "Goal should be for current year"
    assert goal.achieved is False, "Goal should not be achieved initially"


@pytest.mark.asyncio
async def test_create_reading_does_not_duplicate_queue_entry(
    client, create_item, create_reading_status, create_test_session
):
    """
    Test that when creating a second reading for an item already in the queue,
    the queue entry is not duplicated.
    """
    import uuid as uuid_module

    from sqlalchemy import select

    from models.reading import ReadingQueueModel

    item = create_item[0]
    start_date_1 = "2026-01-15"
    start_date_2 = "2026-02-20"
    finish_date_1 = "2026-02-10"

    # Create first reading (completed)
    params = {
        "itemId": item.id,
        "startDate": start_date_1,
        "finishDate": finish_date_1,
    }
    response = await client.post("/reading", json=params)
    assert response.status_code == status.HTTP_201_CREATED

    # Get queue count after first reading
    user_id = uuid_module.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002")
    query = select(ReadingQueueModel).where(
        ReadingQueueModel.owner_id == user_id,
        ReadingQueueModel.item_id == item.id,
        ReadingQueueModel.year == 2026,
    )
    goals_after_first = await create_test_session.execute(query)
    goals_first_list = goals_after_first.scalars().all()
    assert len(goals_first_list) == 1, "Item should have one goal after first reading"

    # Create second reading for the same item
    params = {
        "itemId": item.id,
        "startDate": start_date_2,
    }
    response = await client.post("/reading", json=params)
    assert response.status_code == status.HTTP_201_CREATED

    # Get queue count after second reading
    goals_after_second = await create_test_session.execute(query)
    goals_second_list = goals_after_second.scalars().all()
    assert (
        len(goals_second_list) == 1
    ), "Item should still have only one goal (no duplicate entry)"


@pytest.mark.asyncio
async def test_create_reading_queue_entry_is_year_specific(
    client, create_item, create_reading_status, create_test_session
):
    """
    Test that reading queue entries are year-specific.
    Creating readings in different years should create separate queue entries.
    """
    import uuid as uuid_module

    from sqlalchemy import select

    from models.reading import ReadingQueueModel

    items = create_item
    item_2025 = items[0]
    item_2026 = items[1]

    user_id = uuid_module.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002")

    # Create reading in 2025
    start_date_2025 = "2025-06-15"
    params = {"itemId": item_2025.id, "startDate": start_date_2025}
    response = await client.post("/reading", json=params)
    assert response.status_code == status.HTTP_201_CREATED

    # Create reading in 2026 (current year in tests)
    start_date_2026 = "2026-03-20"
    params = {"itemId": item_2026.id, "startDate": start_date_2026}
    response = await client.post("/reading", json=params)
    assert response.status_code == status.HTTP_201_CREATED

    # Query goals for 2025
    query_2025 = select(ReadingQueueModel).where(
        ReadingQueueModel.owner_id == user_id,
        ReadingQueueModel.item_id == item_2025.id,
        ReadingQueueModel.year == 2025,
    )
    goals_2025_result = await create_test_session.execute(query_2025)
    goals_2025 = goals_2025_result.scalars().all()
    assert len(goals_2025) == 1, "Item should have one goal in 2025"
    assert goals_2025[0].year == 2025

    # Query goals for 2026
    query_2026 = select(ReadingQueueModel).where(
        ReadingQueueModel.owner_id == user_id,
        ReadingQueueModel.item_id == item_2026.id,
        ReadingQueueModel.year == 2026,
    )
    goals_2026_result = await create_test_session.execute(query_2026)
    goals_2026 = goals_2026_result.scalars().all()
    assert len(goals_2026) == 1, "Item should have one goal in 2026"
    assert goals_2026[0].year == 2026
