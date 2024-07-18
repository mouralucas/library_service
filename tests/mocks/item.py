import datetime
import uuid

import pytest_asyncio

from managers.item import ItemManager
from models import ItemModel, ItemStatusModel


@pytest_asyncio.fixture
async def create_item(create_test_session, create_languages,
                      create_series, create_publisher, create_collections, create_authors, create_item_status):
    language = create_languages
    series = create_series
    publisher = create_publisher
    collections = create_collections
    authors = create_authors
    status = create_item_status

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
        last_status_date=datetime.date(2024, 7, 11),
        pages=370,
    )
    item_1 = await ItemManager(session=create_test_session).create_item(item)

    status_item = ItemStatusModel(
        status_id=item_1.last_status_id,
        item_id=item_1.id,
        date=item_1.last_status_date
    )
    await ItemManager(session=create_test_session).add_one(status_item)

    item = ItemModel(
        main_author_id=authors[0].id,
        title="Test Item numero 2",
        subtitle="Test Subtitle do teste 2",
        title_original="Original Title of item 2",
        subtitle_original="Original Subtitle of item 2",
        language_id=language[1].id,
        publisher_id=publisher[1].id,
        serie_id=series[1].id,
        collection_id=collections[1].id,
        owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
        last_status_id=status[0].id,
        last_status_date=datetime.date(2024, 7, 18),
        pages=370,
    )
    item_2 = await ItemManager(session=create_test_session).create_item(item)

    status_item = ItemStatusModel(
        status_id=item_2.last_status_id,
        item_id=item_2.id,
        date=item_2.last_status_date
    )
    await ItemManager(session=create_test_session).add_one(status_item)

    item_list.append(item_1)
    item_list.append(item_2)

    return item_list
