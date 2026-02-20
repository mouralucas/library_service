import uuid
from datetime import date, datetime
from typing import Any

from dateutil.relativedelta import relativedelta
from rolf_common.util.datetime import get_timestamp_aware

from data_mock.core import (
    get_author_mock,
    get_collection_mock,
    get_item_status_mock,
    get_language_mock,
    get_publisher_mock,
    get_serie_mock,
)

default_model_dict = {"created_at": get_timestamp_aware(), "active": True}


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
            "owner_id": uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            "id": 1,
            "main_author_id": authors[0]["id"],
            "title": "O Pistoleiro",
            "title_original": "The Gunslinger",
            "subtitle": "Primeiro livro da série A Torre Negra",
            "language_id": languages[1]["id"],
            "publisher_id": publishers[0]["id"],
            "serie_id": series[1]["id"],
            "collection_id": collections[0]["id"],
            "last_status_id": item_status[0]["id"],
            "last_status_date": date.today() - relativedelta(days=1),
            "type": "book",
            "pages": 262,
        },
        {
            **default_model_dict,
            "owner_id": uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            "id": 2,
            "main_author_id": authors[3]["id"],
            "title": "Coraline",
            "title_original": "Coraline",
            "language_id": languages[1]["id"],
            "publisher_id": publishers[3]["id"],
            "serie_id": series[0]["id"],
            "collection_id": collections[0]["id"],
            "last_status_id": item_status[3]["id"],
            "last_status_date": date.today() - relativedelta(days=4),
            "type": "book",
            "format": "hardcover",
            "pages": 224,
            "publication_date": datetime(2020, 6, 19),
            "original_publication_date": datetime(2002, 7, 2),
        },
        {
            "owner_id": uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
            "id": 3,
            "main_author_id": authors[1]["id"],
            "title": "Neon Genesis Evangelion #01",
            "title_original": "Neon Genesis Evangelion #01",
            "subtitle": "Um dos melhores mangás de ficção científica retorna \
                às bancas em novo formato",
            "pages": 336,
            "publication_date": datetime(2011, 10, 1),
            "original_publication_date": datetime(1995, 8, 29),
            "serie_id": series[2]["id"],
            "language_id": languages[1]["id"],
            "volume": 1,
            "publisher_id": publishers[2]["id"],
            "collection_id": collections[1]["id"],
            "format": "paperback",
            "type": "manga",
            "last_status_id": item_status[0]["id"],
            "last_status_date": date.today() - relativedelta(months=11, days=15),
            "cover_price": 74.90,
            "paid_price": 21.80,
            "isbn": "9786555943412",
        },
    ]

    return items


def get_item_status_relation_mock() -> list[dict[str, Any]]:
    item_status = get_item_status_mock()
    items = get_item_mock()

    item_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": uuid.UUID("5f7d7470-1a23-4fc2-a20a-8a2c1454557c"),
            "status_id": items[0]["last_status_id"],
            "item_id": items[0]["id"],
            "date": items[0]["last_status_date"],
        },
        {
            **default_model_dict,
            "id": uuid.UUID("9c366daf-4be8-4b8d-98c9-a7fdaaea19a9"),
            "status_id": items[1]["last_status_id"],
            "item_id": items[1]["id"],
            "date": items[1]["last_status_date"],
        },
        {
            **default_model_dict,
            "id": uuid.UUID("78b181f6-71ca-4bb6-91a9-1ec70ff110e3"),
            "status_id": items[2]["last_status_id"],
            "item_id": items[2]["id"],
            "date": items[2]["last_status_date"],
        },
    ]

    return item_status


def get_item_author_relation_mock() -> list[dict[str, Any]]:
    items = get_item_mock()

    item_author = [
        {
            **default_model_dict,
            "id": uuid.UUID("ee31e9b1-e7cd-4b4d-aa60-8d99282a0e9c"),
            "item_id": items[0]["id"],
            "author_id": items[0]["main_author_id"],
            "is_main": True,
            "is_translator": False,
        },
        {
            **default_model_dict,
            "id": uuid.UUID("517da74f-7854-4e5a-b2e3-5748f07f5743"),
            "item_id": items[1]["id"],
            "author_id": items[1]["main_author_id"],
            "is_main": True,
            "is_translator": False,
        },
        {
            **default_model_dict,
            "id": uuid.UUID("bc857166-833f-43a9-bb6e-863ed96a34f6"),
            "item_id": items[2]["id"],
            "author_id": items[2]["main_author_id"],
            "is_main": True,
            "is_translator": False,
        },
    ]

    return item_author


def get_item_locations_mock() -> list[dict[str, Any]]:
    locations: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": 0,
            "name": "Não consta",
            "physical_location": "Não consta",
        },
        {
            **default_model_dict,
            "id": 1,
            "name": "Estante 1",
            "physical_location": "Estante 1",
        },
        {
            **default_model_dict,
            "id": 2,
            "name": "Estante 2",
            "physical_location": "Estante 2",
        },
        {
            **default_model_dict,
            "id": 3,
            "name": "Estante 3",
            "physical_location": "Estante 3",
        },
    ]

    return locations
