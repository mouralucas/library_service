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
    create_item_locations,
):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
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
        mutation CreateItem($input: CreateItemInput) {
            createItem(item: $input) {
                created
                id
            }
        }
    """

    variables = {
        "input": {
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
            "itemTypeId": item_type_id,
            "formatId": format_id,
            "locationId": create_item_locations[0].id,
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
    assert "created" in data["data"]["createItem"]
    assert data["data"]["createItem"]["created"] is True
    assert "id" in data["data"]["createItem"]
    assert isinstance(data["data"]["createItem"]["id"], int)
