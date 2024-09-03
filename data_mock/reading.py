import datetime
from typing import Any
import uuid

from dateutil.relativedelta import relativedelta

from data_mock.core import get_reading_status_mocked
from data_mock.item import get_item_mocked

default_model_dict = {
    'created_at': datetime.datetime.utcnow(),
    'active': True
}

def get_one_reading() -> dict[str, Any]:
    items = get_item_mocked()
    reading_status = get_reading_status_mocked()

    reading: dict[str, Any] = {
        **default_model_dict,
        'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
        'id': uuid.UUID('49692845-f01e-4b41-b643-61bae72a7e2b'),
        'item_id': items[0]['id'],
        'start_date': datetime.datetime.utcnow() + relativedelta(days=24),
        'status_id': reading_status[0]['id'],
    }

    return reading

