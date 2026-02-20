import copy

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_item_success(
    client,
    create_languages,
    create_series,
    create_item_status,
    create_publisher,
    create_collections,
    create_authors,
    create_item_locations,
):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    pages = 756
    last_status_date = "2024-06-01"
    cover_price = 110.15
    paid_price = 57.90

    languages = create_languages
    series = create_series
    publishers = create_publisher
    collections = create_collections
    authors = create_authors
    list_item_status = create_item_status

    payload = {
        "mainAuthorId": authors[0].id,
        "otherAuthorsId": [authors[1].id, authors[2].id],
        "title": item_title,
        "subtitle": item_subtitle,
        "pages": pages,
        "languageId": languages[0].id,
        "publisherId": publishers[0].id,
        "serieId": series[0].id,
        "collectionId": collections[0].id,
        "lastStatusId": list_item_status[0].id,
        "lastStatusDate": last_status_date,
        "coverPrice": cover_price,
        "paidPrice": paid_price,
        "locationId": create_item_locations[0].id,
    }

    mutation = """
        mutation CreateItem($item: CreateItemInput) {
            createItem(item: $item) {
                id
                created
            }
        }
    """
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": {"item": payload}}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createItem" in data["data"]

    data = data["data"]["createItem"]
    assert "created" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_create_item_without_non_required(
    client,
    create_languages,
    create_item_status,
    create_authors,
    create_series,
    create_collections,
    create_item_locations,
):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    last_status_date = "2024-06-01"

    languages = create_languages
    authors = create_authors
    list_item_status = create_item_status

    payload = {
        "mainAuthorId": authors[0].id,
        "title": item_title,
        "subtitle": item_subtitle,
        "languageId": languages[0].id,
        "lastStatusId": list_item_status[0].id,
        "lastStatusDate": last_status_date,
        "locationId": create_item_locations[0].id,
    }
    mutation = """
        mutation CreateItem($item: CreateItemInput) {
            createItem(item: $item) {
                id
                created
            }
        }
    """
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": {"item": payload}}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createItem" in data["data"]

    data = data["data"]["createItem"]
    assert "created" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_update_item(client, create_item, create_item_locations):
    items = create_item

    old_item = copy.deepcopy(items[0])
    new_title = "Updated title"
    new_pages = 100
    new_status_id = "bought"
    new_last_status_date = "2024-07-12"

    payload = {
        "id": old_item.id,
        "title": new_title,
        "pages": new_pages,
        "lastStatusId": new_status_id,
        "lastStatusDate": new_last_status_date,
        "locationId": create_item_locations[0].id,
    }
    response = await client.patch("/item", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "created" in data
    assert data["created"] is True


@pytest.mark.asyncio
async def test_get_all_items(client, create_item):
    items = create_item
    items_list_len = len(items)

    title = items[0].title
    pages = items[0].pages

    response = await client.get("/item")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert type(data["items"]) is list
    assert len(data["items"]) == items_list_len
    assert data["items"][0]["title"] == title
    assert data["items"][0]["pages"] == pages


@pytest.mark.asyncio
async def test_get_item_with_title_exist_filter(client, create_item):
    items = create_item

    # Test if title exists
    param = {
        "title": items[0].title,
    }
    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                items {
                    id
                    mainAuthorId
                    mainAuthorName
                    title
                    subtitle
                    titleOriginal
                    subtitleOriginal
                    isbn
                    isbn10
                    itemTypeId
                    pages
                    volume
                    edition
                    publicationDate
                    originalPublicationDate
                    serieId
                    serieName
                    collectionId
                    collectionName
                    publisherId
                    publisherName
                    formatId
                    languageId
                    languageName
                    coverPrice
                    paidPrice
                    lastStatusId
                    lastStatusName
                    lastStatusDate
                }
                quantity
            }
        }

    """
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": {"params": param}}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    data = data["data"]["getItems"]

    assert "items" in data
    assert "quantity" in data

    assert data["items"][0]["title"] == items[0].title
    assert data["items"][0]["pages"] == items[0].pages


@pytest.mark.asyncio
async def test_get_item_with_title_not_exist_filter(client, create_item):
    # test if title does not exist
    param = {
        "title": "title not exists",
    }
    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                items {
                    id
                    mainAuthorId
                    mainAuthorName
                    title
                    subtitle
                    titleOriginal
                    subtitleOriginal
                    isbn
                    isbn10
                    itemTypeId
                    pages
                    volume
                    edition
                    publicationDate
                    originalPublicationDate
                    serieId
                    serieName
                    collectionId
                    collectionName
                    publisherId
                    publisherName
                    formatId
                    languageId
                    languageName
                    coverPrice
                    paidPrice
                    lastStatusId
                    lastStatusName
                    lastStatusDate
                }
                quantity
            }
        }

    """
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": {"params": param}}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    data = data["data"]["getItems"]

    assert "items" in data
    assert "quantity" in data
    assert data["quantity"] == 0
    assert data["items"] is None


@pytest.mark.asyncio
async def test_get_item_with_id_exist_filter(client, create_item):
    items = create_item

    # Test with id fiter
    param = {
        "itemId": items[0].id,
    }
    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                items {
                    id
                    mainAuthorId
                    mainAuthorName
                    title
                    subtitle
                    titleOriginal
                    subtitleOriginal
                    isbn
                    isbn10
                    itemTypeId
                    pages
                    volume
                    edition
                    publicationDate
                    originalPublicationDate
                    serieId
                    serieName
                    collectionId
                    collectionName
                    publisherId
                    publisherName
                    formatId
                    languageId
                    languageName
                    coverPrice
                    paidPrice
                    lastStatusId
                    lastStatusName
                    lastStatusDate
                }
                quantity
            }
        }

    """
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": {"params": param}}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    data = data["data"]["getItems"]

    assert "items" in data
    assert "quantity" in data

    assert data["items"][0]["title"] == items[0].title
    assert data["items"][0]["pages"] == items[0].pages


@pytest.mark.asyncio
async def test_get_item_id_out_range(client, create_item):
    # Test with id off the range
    param = {
        "itemId": 0,
    }
    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                items {
                    id
                    mainAuthorId
                    mainAuthorName
                    title
                    subtitle
                    titleOriginal
                    subtitleOriginal
                    isbn
                    isbn10
                    itemTypeId
                    pages
                    volume
                    edition
                    publicationDate
                    originalPublicationDate
                    serieId
                    serieName
                    collectionId
                    collectionName
                    publisherId
                    publisherName
                    formatId
                    languageId
                    languageName
                    coverPrice
                    paidPrice
                    lastStatusId
                    lastStatusName
                    lastStatusDate
                }
                quantity
            }
        }

    """
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": {"params": param}}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "errors" in data
