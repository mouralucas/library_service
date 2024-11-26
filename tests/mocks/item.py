import pytest_asyncio
from rolf_common.managers import BaseDataManager
from rolf_common.models import SQLModel

from data_mock.item import get_item_mock, get_item_status_relation_mock
from models import ItemModel, ItemStatusModel
from schemas.item import ItemSchema


@pytest_asyncio.fixture
async def create_item(create_test_session, create_languages,
                      create_series, create_publisher,
                      create_collections, create_authors, create_item_status) -> list[ItemSchema]:
    data_: list[SQLModel] = await BaseDataManager(create_test_session).add_or_ignore_all(ItemModel, get_item_mock())
    item_list: list[ItemSchema] = [ItemSchema.model_validate(data['ItemModel']) for data in data_]

    await BaseDataManager(create_test_session).add_or_ignore_all(ItemStatusModel, get_item_status_relation_mock())

    return item_list
