import pytest_asyncio
from rolf_common.managers import BaseDataManager

from data_mock.reading import get_active_reading_mocked, get_reading_progress_mocked, get_reading_list_one_active_mocked
from models import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema, ProgressSchema


@pytest_asyncio.fixture
async def create_more_than_one_reading(create_test_session, create_item, create_reading_status):
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(ReadingModel, get_reading_list_one_active_mocked())
    readings = [ReadingSchema.model_validate(data['ReadingModel']) for data in data_]

    return readings


@pytest_asyncio.fixture
async def create_active_active_readings(create_test_session, create_item, create_reading_status) -> list[ReadingSchema]:
    """
        This fixture create active readings from different items.
        It can create any numbers of readings as it's necessary, but to maintain integrity of the business rules, each active reading must have
         its own item. One item cannot be in more than one active reading.
    :param create_test_session:
    :param create_item:
    :param create_reading_status:
    :return: the list of active readings
    """
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(ReadingModel, get_active_reading_mocked())
    readings = [ReadingSchema.model_validate(data['ReadingModel']) for data in data_]

    return readings


@pytest_asyncio.fixture
async def create_progress(create_test_session, create_active_active_readings) -> list[ProgressSchema]:
    data_ = await BaseDataManager(create_test_session).add_or_ignore_all(ReadingProgressModel, get_reading_progress_mocked())
    progress = [ProgressSchema.model_validate(data['ReadingProgressModel']) for data in data_]

    return progress
