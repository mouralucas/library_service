import pytest
from fastapi import status

from tests.mocks.core import *
from tests.mocks.item import create_item


@pytest.mark.asyncio
async def test_create_item_success(client, create_languages, create_series, create_status,
                                   create_publisher, create_collections, create_authors):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    item_original_title = "Test item original title"
    item_original_subtitle = "Test item original subtitle"

    languages = create_languages
    series = create_series
    publishers = create_publisher
    collections = create_collections
    authors = create_authors
    list_status = create_status

    payload = {
        'mainAuthorId': authors[0].id,
        'title': item_title,
        'subtitle': item_subtitle,
        'originalTitle': item_original_title,
        'originalSubtitle': item_original_subtitle,
        'languageId': languages[0].id,
        'publisherId': publishers[0].id,
        'serieId': series[0].id,
        'collectionId': collections[0].id,
        'lastStatusId': list_status[0].id,
    }
    response = await client.post('/item', json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'item' in data
    assert type(data['item']) is dict


@pytest.mark.asyncio
async def test_get_item(client, create_item):
    items = create_item
    items_list_len = len(items)

    response = await client.get('/item')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'items' in data
    assert type(data['items']) is list
    assert len(data['items']) == items_list_len
