import datetime
import uuid
from typing import List, Type

import pytest_asyncio
from rolf_common.models import SQLModel

from managers.reading import ReadingDataManager
from models import ReadingModel, ReadingProgressModel


@pytest_asyncio.fixture
async def create_one_reading(create_test_session, create_item, create_reading_status):
    item = create_item
    reading_list = []

    reading = ReadingModel(item_id=item[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2020, 1, 1),
                           status_id='reading')
    reading_1 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    return reading_1


@pytest_asyncio.fixture
async def create_more_than_one_reading(create_test_session, create_item, create_reading_status):
    item = create_item
    reading_list = []

    reading = ReadingModel(item_id=item[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2020, 1, 1),
                           finish_date=datetime.date(2020, 1, 20),
                           active=False,
                           status_id='read')
    reading_1 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    reading = ReadingModel(item_id=item[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2021, 1, 1),
                           status_id='reading')
    reading_2 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    reading_list.append(reading_1)
    reading_list.append(reading_2)

    return reading_list


@pytest_asyncio.fixture
async def create_active_active_readings(create_test_session, create_item, create_reading_status) -> list[SQLModel]:
    """
        This fixture create active readings from different items.
        It can create any numbers of readings as it's necessary, but to maintain integrity of the business rules, each active reading must have
         its own item. One item cannot be in more than one active reading.
    :param create_test_session:
    :param create_item:
    :param create_reading_status:
    :return: the list of active readings
    """
    items = create_item
    reading_list = []

    reading = ReadingModel(item_id=items[0].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2021, 1, 1),
                           status_id='reading')
    reading_1 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    reading = ReadingModel(item_id=items[1].id, owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                           start_date=datetime.date(2021, 1, 1),
                           status_id='reading')
    reading_2 = await ReadingDataManager(session=create_test_session).create_reading(reading)

    reading_list.append(reading_1)
    reading_list.append(reading_2)

    return reading_list


@pytest_asyncio.fixture
async def create_progress(create_test_session, create_one_reading):
    readings = create_one_reading

    progress_list = []

    progress = ReadingProgressModel(reading_id=readings.id, date=datetime.date(2024, 5, 1), page=37, percentage=10)
    progress_1 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress = ReadingProgressModel(reading_id=readings.id, date=datetime.date(2024, 5, 2), page=74, percentage=20)
    progress_2 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress = ReadingProgressModel(reading_id=readings.id, date=datetime.date(2024, 5, 3), page=111, percentage=30)
    progress_3 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress_list.append(progress_1)
    progress_list.append(progress_2)
    progress_list.append(progress_3)

    return progress_list
