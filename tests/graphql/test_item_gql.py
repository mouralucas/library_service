import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_mutation_new_item_success(
    client,
    create_languages,
    create_series,
    create_item_status,
    create_publisher,
    create_collections,
    create_authors,
):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    item_original_title = "Test item original title"
    item_original_subtitle = "Test item original subtitle"
    pages = 756
    last_status_date = "2024-06-01"
    cover_price = 110.15
    paid_price = 57.90
    item_type_id = "book"
    format_id = "hardcover"

    languages = create_languages
    series = create_series
    publishers = create_publisher
    collections = create_collections
    authors = create_authors
    list_item_status = create_item_status

    mutation = """
        mutation CreateItem($input: CreateItemInput!) {
            createItem(item: $input) {
                item {
                    id
                    title
                    itemTypeId
                    formatId
                }
            }
        }
    """

    variables = {
        "input": {
            "mainAuthorId": authors[0].id,
            "otherAuthorsId": [authors[1].id, authors[2].id],
            "title": item_title,
            "subtitle": item_subtitle,
            "titleOriginal": item_original_title,
            "subtitleOriginal": item_original_subtitle,
            "pages": pages,
            "languageId": languages[0].id,
            "publisherId": publishers[0].id,
            "serieId": series[0].id,
            "collectionId": collections[0].id,
            "lastStatusId": list_item_status[0].id,
            "lastStatusDate": last_status_date,
            "coverPrice": cover_price,
            "paidPrice": paid_price,
            "itemTypeId": item_type_id,
            "formatId": format_id,
        }
    }

    # Chamando o endpoint do GraphQL
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # Validação da resposta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert "createItem" in data["data"]
    assert "item" in data["data"]["createItem"]

    item = data["data"]["createItem"]["item"]
    assert item["title"] == item_title
    assert item["itemTypeId"] == item_type_id
    assert item["formatId"] == format_id


@pytest.mark.asyncio
async def test_query_books(client, create_item):
    items = create_item
    books = list(filter(lambda item: item.type == "book", items))

    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                quantity
                items {
                    itemId
                    title
                    itemTypeId
                }
            }
        }
    """

    variables = {"params": {"itemTypeId": "book"}}

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    assert "quantity" in data["data"]["getItems"]
    assert data["data"]["getItems"]["quantity"] == len(books)

    assert "items" in data["data"]["getItems"]
    items_data = data["data"]["getItems"]["items"]

    for item in items_data:
        assert "itemId" in item
        assert "title" in item

        assert "itemTypeId" in item
        assert item["itemTypeId"] == "book"


@pytest.mark.asyncio
async def test_query_books_with_order_by(client, create_item):
    items = create_item
    books = list(filter(lambda item: item.type == "book", items))

    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                quantity
                items {
                    itemId
                    title
                    itemTypeId
                }
            }
        }
    """

    variables = {
        "params": {
            "itemTypeId": "book",
            "orderBy": [{"field": "title", "direction": "ASC"}],
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    assert "quantity" in data["data"]["getItems"]
    assert data["data"]["getItems"]["quantity"] == len(books)
