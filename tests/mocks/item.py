import uuid

import pytest_asyncio

from managers.item import ItemManager
from models import ItemModel


@pytest_asyncio.fixture
async def create_item(create_test_session, create_languages,
                      create_series, create_publisher, create_collections, create_authors, create_status):
    language = create_languages
    series = create_series
    publisher = create_publisher
    collections = create_collections
    authors = create_authors
    status = create_status

    item_list = []

    item = ItemModel(
        main_author_id=authors[0].id,
        title="Test Item",
        subtitle="Test Subtitle",
        title_original="Original Title",
        subtitle_original="Original Subtitle",
        language_id=language[0].id,
        publisher_id=publisher[0].id,
        serie_id=series[0].id,
        collection_id=collections[0].id,
        owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
        last_status_id=status[0].id,
    )
    item_1 = await ItemManager(session=create_test_session).create_item(item)

    # item = ItemModel()
    # item_2 = await ItemManager(session=create_test_session).create_item(item)

    item_list.append(item_1)
    # item_list.append(item_2)

    return item_list
