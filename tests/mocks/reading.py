import datetime
import uuid

import pytest_asyncio

from managers.reading import ReadingDataManager
from models import ReadingModel, ReadingProgressModel


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


@pytest_asyncio.fixture
async def create_progress(create_test_session, create_reading):
    readings = create_reading

    progress_list = []

    progress = ReadingProgressModel(reading_id=readings[0].id, date=datetime.date(2024, 5, 1), page=37, percentage=10)
    progress_1 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress = ReadingProgressModel(reading_id=readings[0].id, date=datetime.date(2024, 5, 2), page=74, percentage=20)
    progress_2 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress = ReadingProgressModel(reading_id=readings[0].id, date=datetime.date(2024, 5, 2), page=111, percentage=30)
    progress_3 = await ReadingDataManager(session=create_test_session).create_progress(progress)

    progress_list.append(progress_1)
    progress_list.append(progress_2)
    progress_list.append(progress_3)

    return progress_list