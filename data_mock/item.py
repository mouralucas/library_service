import datetime
import random
import uuid
from typing import Any

from dateutil.relativedelta import relativedelta
from sqlalchemy.sql.functions import random

from data_mock.core import get_author_mock, get_language_mock, get_publisher_mock, get_serie_mock, get_collection_mock, get_item_status_mock

default_model_dict = {
    'created_at': datetime.datetime.now(datetime.timezone.utc),
    'active': True
}


def get_item_mock() -> list[dict[str, Any]]:
    authors = get_author_mock()
    languages = get_language_mock()
    publishers = get_publisher_mock()
    series = get_serie_mock()
    collections = get_collection_mock()
    item_status = get_item_status_mock()

    items: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': 1,
            'main_author_id': authors[0]['id'],
            'title': 'Esse é o título',
            'subtitle': 'E esse é o subtítulo',
            'language_id': languages[0]['id'],
            'publisher_id': publishers[0]['id'],
            'serie_id': series[0]['id'],
            'collection_id': collections[0]['id'],
            'last_status_id': item_status[0]['id'],
            'last_status_date': datetime.date.today() - relativedelta(days=1),
            'pages': 370
        },
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': 2,
            'main_author_id': authors[0]['id'],
            'title': 'Esse é o título do outro livro',
            'subtitle': 'E essa o outro subtítulo',
            'language_id': languages[1]['id'],
            'publisher_id': publishers[1]['id'],
            'serie_id': series[1]['id'],
            'collection_id': collections[1]['id'],
            'last_status_id': item_status[1]['id'],
            'last_status_date': datetime.date.today() - relativedelta(days=4),
            'pages': 570
        }
    ]

    return items


def get_item_status_relation_mock() -> list[dict[str, Any]]:
    item_status = get_item_status_mock()
    items = get_item_mock()

    item_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': uuid.UUID('5f7d7470-1a23-4fc2-a20a-8a2c1454557c'),
            'status_id': item_status[0]['id'],
            'item_id': items[0]['id'],
            'date': items[0]['last_status_date'],
        },
        {
            **default_model_dict,
            'id': uuid.UUID('9c366daf-4be8-4b8d-98c9-a7fdaaea19a9'),
            'status_id': item_status[1]['id'],
            'item_id': items[1]['id'],
            'date': items[1]['last_status_date'],
        }
    ]

    return item_status


def get_item_author_relation_mock() -> list[dict[str, Any]]:
    items = get_item_mock()
    authors = get_author_mock()

    item_author = [
        {
            **default_model_dict,
            'id': uuid.UUID("ee31e9b1-e7cd-4b4d-aa60-8d99282a0e9c"),
            'item_id': items[0]['id'],
            'author_id': authors[0]['id'],
            'is_main': True,
            'is_translator': False
        },
        {
            **default_model_dict,
            'id': uuid.UUID('517da74f-7854-4e5a-b2e3-5748f07f5743'),
            'item_id': items[1]['id'],
            'author_id': authors[0]['id'],
            'is_main': True,
            'is_translator': False
        }
    ]

    return item_author