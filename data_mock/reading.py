import datetime
import uuid
from typing import Any

from dateutil.relativedelta import relativedelta

from data_mock.core import get_reading_status_mock
from data_mock.item import get_item_mock

default_model_dict = {
    'created_at': datetime.datetime.utcnow(),
    'active': True
}


def get_active_reading_mocked() -> list[dict[str, Any]]:
    items = get_item_mock()
    reading_status = get_reading_status_mock()

    reading: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('49692845-f01e-4b41-b643-61bae72a7e2b'),
            'item_id': items[0]['id'],
            'start_date': datetime.datetime.utcnow() - relativedelta(days=24),
            'status_id': reading_status[0]['id'],
        },
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('606c2816-c863-4859-b9a7-0e39a3af2466'),
            'item_id': items[1]['id'],
            'start_date': datetime.datetime.utcnow() + relativedelta(days=15),
            'status_id': reading_status[0]['id'],
        }
    ]

    return reading


def get_reading_list_one_active_mocked() -> list[dict[str, Any]]:
    items = get_item_mock()
    reading_status = get_reading_status_mock()

    readings: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('5e3e5314-2406-4637-b98c-7afab5d9cefc'),
            'item_id': items[0]['id'],
            'start_date': datetime.datetime.utcnow() + relativedelta(months=1, days=2),
            'finish_date': datetime.datetime.utcnow() + relativedelta(days=15),
            'active': False,
            'status_id': reading_status[1]['id'],
        },
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('d9c5b128-b525-4f61-85d6-9fe981711093'),
            'item_id': items[0]['id'],
            'start_date': datetime.datetime.utcnow() + relativedelta(days=12),
            'status_id': reading_status[0]['id'],
        }
    ]

    return readings


def get_reading_progress_mocked() -> list[dict[str, Any]]:
    active_reading = get_active_reading_mocked()

    progress: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': uuid.UUID('767071bc-9dfd-4aae-ac7c-a6eb589f6029'),
            'reading_id': active_reading[0]['id'],
            'item_id': active_reading[0]['item_id'],
            'date': datetime.datetime.utcnow() - relativedelta(days=25),
            'page': 37,
            'percentage': 10
        },
        {
            **default_model_dict,
            'id': uuid.UUID('767071bc-9dfd-4aae-ac7c-a6eb589f6029'),
            'reading_id': active_reading[0]['id'],
            'item_id': active_reading[0]['item_id'],
            'date': datetime.datetime.utcnow() - relativedelta(days=20),
            'page': 74,
            'percentage': 20
        },
        {
            **default_model_dict,
            'id': uuid.UUID('767071bc-9dfd-4aae-ac7c-a6eb589f6029'),
            'reading_id': active_reading[0]['id'],
            'item_id': active_reading[0]['item_id'],
            'date': datetime.datetime.utcnow() - relativedelta(days=15),
            'page': 111,
            'percentage': 30
        }
    ]

    return progress
