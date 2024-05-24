import datetime
import uuid

import pytest_asyncio

from managers.reading import ReadingDataManager
from models import ReadingModel
from tests.mocks.item import create_item


@pytest_asyncio.fixture
async def create_reading(create_test_session, create_item):
    item = create_item
    reading_list = []

    reading = ReadingModel(item_id=item[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2020, 1, 1),
                           status_id='reading')
    reading_1 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    reading_list.append(reading_1)

    return reading_list
