from typing import Any
import uuid

from sqlalchemy.sql.functions import random

from data_mock.core import get_author_mocked, get_language_mocked, get_publisher_mocked, get_serie_mocked, get_collection_mocked, get_item_status_mocked
import datetime
from dateutil.relativedelta import relativedelta

default_model_dict = {
    'created_at': datetime.datetime.utcnow(),
    'active': True
}


def get_item_mocked() -> list[dict[str, Any]]:
    authors = get_author_mocked()
    languages = get_language_mocked()
    publishers = get_publisher_mocked()
    series = get_serie_mocked()
    collections = get_collection_mocked()
    item_status = get_item_status_mocked()

    items: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('6fa72c33-4849-4877-8e74-176a94f93298'),
            'main_author_id': authors[0]['id'],
            'title': 'Esse é o título',
            'subtitle': 'E esse é o subtítulo',
            'language_id': languages[0]['id'],
            'publisher_id': publishers[0]['id'],
            'serie_id': series[0]['id'],
            'collection_id': collections[0]['id'],
            'last_status_id': item_status[0]['id'],
            'last_status_date': datetime.date.today() - relativedelta(days=1),
            'page': random.randrange(300, 1500)
        },
        {
            **default_model_dict,
            'owner_id': uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            'id': uuid.UUID('2e2fd377-ceec-43be-aad6-2b02aa7f8c3b'),
            'main_author_id': authors[0]['id'],
            'title': 'Esse é o título do outro livro',
            'description': 'E essa o outro subtítulo',
            'language_id': languages[1]['id'],
            'publisher_id': publishers[1]['id'],
            'serie_id': series[1]['id'],
            'collection_id': collections[1]['id'],
            'last_status_id': item_status[1]['id'],
            'last_status_date': datetime.date.today() - relativedelta(days=4),
            'page': random.randrange(150, 1000)
        }
    ]

    return items


def get_item_status_relation_mocked() -> list[dict[str, Any]]:
    item_status = get_item_status_mocked()
    items = get_item_mocked()

    item_status: list[dict[str, Any]] = [
        {
            'status_id': item_status[0]['id'],
            'item_id': items[0]['id'],
            'date': items[0]['last_status_date'],
        },
        {
            'status_id': item_status[1]['id'],
            'item_id': items[1]['id'],
            'date': items[1]['last_status_date'],
        }
    ]

    return item_status
