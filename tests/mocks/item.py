from typing import Any

import pytest_asyncio
from rolf_common.managers import BaseDataManager

from data_mock.item import get_item_locations_mock, get_item_mock, get_item_status_relation_mock
from models import ItemModel, ItemStatusModel
from models.item import ItemLocationModel
from schemas.item import ItemSchema


@pytest_asyncio.fixture
async def create_item(
    create_test_session,
    create_languages,
    create_series,
    create_publisher,
    create_collections,
    create_authors,
    create_item_status,
) -> list[ItemSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        ItemModel, get_item_mock()
    )
    item_list: list[ItemSchema] = (
        [ItemSchema.model_validate(data["ItemModel"]) for data in data_]
        if data_
        else []
    )

    await BaseDataManager(create_test_session).add_or_ignore_all(
        ItemStatusModel, get_item_status_relation_mock()
    )

    return item_list


@pytest_asyncio.fixture
async def create_item_locations(create_test_session) -> list[dict[str, Any]]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(
        ItemLocationModel, get_item_locations_mock()
    )
    item_locations: list[dict[str, Any]] = (
        [data["ItemLocationModel"] for data in data_] if data_ else []
    )

    return item_locations