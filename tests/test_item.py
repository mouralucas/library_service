import copy

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_item_success(client, create_languages, create_series, create_item_status,
                                   create_publisher, create_collections, create_authors):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    item_original_title = "Test item original title"
    item_original_subtitle = "Test item original subtitle"
    pages = 756
    last_status_date = '2024-06-01'
    cover_price = 110.15
    paid_price = 57.90

    languages = create_languages
    series = create_series
    publishers = create_publisher
    collections = create_collections
    authors = create_authors
    list_item_status = create_item_status

    payload = {
        'mainAuthorId': authors[0].id,
        'otherAuthorsId': [authors[1].id, authors[2].id],
        'title': item_title,
        'subtitle': item_subtitle,
        'originalTitle': item_original_title,
        'originalSubtitle': item_original_subtitle,
        'pages': pages,
        'languageId': languages[0].id,
        'publisherId': publishers[0].id,
        'serieId': series[0].id,
        'collectionId': collections[0].id,
        'lastStatusId': list_item_status[0].id,
        'lastStatusDate': last_status_date,
        'coverPrice': cover_price,
        'paidPrice': paid_price,
    }

    headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
    response = await client.post('/item', json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'item' in data
    assert type(data['item']) is dict

    # Basic item validation
    assert 'itemId' in data['item']
    assert 'title' in data['item']
    assert data['item']['title'] == item_title

    assert 'subtitle' in data['item']
    assert data['item']['subtitle'] == item_subtitle

    assert 'pages' in data['item']
    assert data['item']['pages'] == pages

    # Author validation
    assert 'mainAuthorId' in data['item']
    assert data['item']['mainAuthorId'] == authors[0].id

    # TODO: removed selectin from models, so analyse the need to return this data
    # assert 'mainAuthor' in data['item']
    # assert 'authorId' in data['item']['mainAuthor']
    # assert data['item']['mainAuthor']['authorId'] == authors[0].id
    # assert 'authorName' in data['item']['mainAuthor']
    # assert data['item']['mainAuthor']['authorName'] == authors[0].name

    # Publisher validation (not required)
    assert 'publisherId' in data['item']
    assert data['item']['publisherId'] == publishers[0].id

    # assert 'publisher' in data['item']
    # assert 'publisherId' in data['item']['publisher']
    # assert data['item']['publisher']['publisherId'] == publishers[0].id
    # assert 'publisherName' in data['item']['publisher']
    # assert data['item']['publisher']['publisherName'] == publishers[0].name

    # Series validation (it's not required, but have default value)
    assert 'serieId' in data['item']
    assert data['item']['serieId'] == series[0].id

    # assert 'serie' in data['item']
    # assert 'serieName' in data['item']['serie']
    # assert data['item']['serie']['serieId'] == series[0].id
    # assert 'serieName' in data['item']['serie']
    # assert data['item']['serie']['serieName'] == series[0].name

    # Collection validation (it's not required, but have default value)
    assert 'collectionId' in data['item']
    assert data['item']['collectionId'] == collections[0].id

    # assert 'collection' in data['item']
    # assert 'collectionId' in data['item']['collection']
    # assert data['item']['collection']['collectionId'] == collections[0].id
    # assert 'collectionName' in data['item']['collection']
    # assert data['item']['collection']['collectionName'] == collections[0].name

    # Last status validation
    assert 'lastStatusId' in data['item']
    assert data['item']['lastStatusId'] == list_item_status[0].id

    # assert 'lastStatus' in data['item']
    # assert 'statusId' in data['item']['lastStatus']
    # assert data['item']['lastStatus']['statusId'] == list_item_status[0].id
    # assert 'statusName' in data['item']['lastStatus']
    # assert data['item']['lastStatus']['statusName'] == list_item_status[0].name

    assert 'lastStatusDate' in data['item']
    assert data['item']['lastStatusDate'] == last_status_date

    # Price validation
    assert 'coverPrice' in data['item']
    assert data['item']['coverPrice'] == cover_price

    assert 'paidPrice' in data['item']
    assert data['item']['paidPrice'] == paid_price


@pytest.mark.asyncio
async def test_create_item_without_non_required(client, create_languages, create_item_status, create_authors, create_series, create_collections):
    item_title = "Test item"
    item_subtitle = "Test subtitle"
    item_original_title = "Test item original title"
    item_original_subtitle = "Test item original subtitle"
    last_status_date = '2024-06-01'

    languages = create_languages
    authors = create_authors
    list_item_status = create_item_status

    payload = {
        'mainAuthorId': authors[0].id,
        'title': item_title,
        'subtitle': item_subtitle,
        'originalTitle': item_original_title,
        'originalSubtitle': item_original_subtitle,
        'languageId': languages[0].id,
        'lastStatusId': list_item_status[0].id,
        'lastStatusDate': last_status_date,
    }

    headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
    response = await client.post('/item', json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    # Default publisher validation
    assert 'publisherId' not in data['item']

    # Default serie validation
    assert 'serieId' in data['item']
    assert data['item']['serieId'] == 0

    # Default collection validation
    assert 'collectionId' in data['item']
    assert data['item']['collectionId'] == 0

    # Default pages validation
    assert 'pages' in data['item']
    assert data['item']['pages'] == 0

    # Default price validation
    assert 'coverPrice' in data['item']
    assert data['item']['coverPrice'] == 0.0

    assert 'paidPrice' in data['item']
    assert data['item']['paidPrice'] == 0.0


@pytest.mark.asyncio
async def test_update_item(client, create_item):
    items = create_item

    old_item = copy.deepcopy(items[0])
    new_title = 'Updated title'
    new_pages = 100
    new_status_id = 'bought'
    new_last_status_date = '2024-07-12'

    payload = {
        'itemId': old_item.id,
        'title': new_title,
        'pages': new_pages,
        'lastStatusId': new_status_id,
        'lastStatusDate': new_last_status_date,
    }
    response = await client.patch('/item', json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'item' in data

    assert 'itemId' in data['item']
    assert data['item']['itemId'] == old_item.id

    assert 'title' in data['item']
    assert data['item']['title'] == new_title
    assert data['item']['title'] != old_item.title

    assert 'pages' in data['item']
    assert data['item']['pages'] == new_pages
    assert data['item']['pages'] != old_item.pages


@pytest.mark.asyncio
async def test_get_all_items(client, create_item):
    items = create_item
    items_list_len = len(items)

    title = items[0].title
    pages = items[0].pages

    response = await client.get('/item')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'items' in data
    assert type(data['items']) is list
    assert len(data['items']) == items_list_len
    assert data['items'][0]['title'] == title
    assert data['items'][0]['pages'] == pages


@pytest.mark.asyncio
async def test_get_item_with_filter(client, create_item):
    items = create_item

    # Test if title exists
    param = {
        'title': items[0].title,
    }
    response = await client.get('/item', params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'items' in data
    assert 'quantity' in data

    assert data['items'][0]['title'] == items[0].title
    assert data['items'][0]['pages'] == items[0].pages

    # test if title does not exist
    param = {
        'title': "title not exists",
    }
    response = await client.get('/item', params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'items' in data
    assert 'quantity' in data
    assert data['quantity'] == 0

    # Test with id fiter
    param = {
        'itemId': items[0].id,
    }
    response = await client.get('/item', params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'items' in data
    assert 'quantity' in data
    assert data['quantity'] == 1

    assert data['items'][0]['itemId'] == items[0].id

    # Test with id that not exists
    param = {
        'itemId': 1000,
    }
    response = await client.get('/item', params=param)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'items' in data
    assert 'quantity' in data
    assert data['quantity'] == 0

    # Test with id off the range
    param = {
        'itemId': 0,
    }
    response = await client.get('/item', params=param)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
