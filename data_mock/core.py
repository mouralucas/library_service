from typing import Any
import uuid
import datetime

default_model_dict = {
    'created_at': datetime.datetime.utcnow(),
    'active': True
}


def get_item_status_mocked() -> list[dict[str, Any]]:
    item_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 'owned',
            'name': 'Na estante',
            'type': 'ITEM.STATUS'
        },
        {
            **default_model_dict,
            'id': 'bought',
            'name': 'Comprado',
            'type': 'ITEM.STATUS'
        },
        {
            **default_model_dict,
            'id': 'sold',
            'name': 'Vendido',
            'type': 'ITEM.STATUS'
        }
    ]

    return item_status


def get_reading_status_mocked() -> list[dict[str, Any]]:
    reading_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 'reading',
            'name': 'Lendo',
            'type': 'READING.STATUS'
        },
        {
            **default_model_dict,
            'id': 'read',
            'name': 'Lido',
            'type': 'READING.STATUS'
        }
    ]

    return reading_status


def get_language_mocked() -> list[dict[str, Any]]:
    languages: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 'EN',
            'name': 'Inglês',
            'code': 'EN'
        },
        {
            **default_model_dict,
            'id': 'PT',
            'name': 'Português',
            'code': 'PT'
        }
    ]

    return languages


def get_country_mocked() -> list[dict[str, Any]]:
    countries: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 'BR',
            'name': 'Brasil',
            'continent': 'SA',
        },
        {
            **default_model_dict,
            'id': 'DE',
            'name': 'Alemanha',
            'continent': 'EU',
        },
        {
            **default_model_dict,
            'id': 'AU',
            'name': 'Austrália',
            'continent': 'OC',
        }
    ]

    return countries


def get_serie_mocked() -> list[dict[str, Any]]:
    series: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 0,
            'name': 'Não consta',
            'description': 'Não pertence a nenhuma série específica',
        },
        {
            **default_model_dict,
            'id': 1,
            'name': 'Série de teste',
            'description': 'Essa é a descrição da série de teste'
        },
        {
            **default_model_dict,
            'id': 2,
            'name': 'Outra série de teste',
            'description': 'Essa é a descrição da outra série'
        }
    ]

    return series


def get_collection_mocked() -> list[dict[str, Any]]:
    collections: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 0,
            'name': 'Não consta',
            'description': 'Não pertence a nenhuma coleção específica'
        },
        {
            **default_model_dict,
            'id': 1,
            'name': 'Coleção de teste',
            'description': 'A descrição da coleção de teste'
        },
        {
            **default_model_dict,
            'id': 2,
            'name': 'Outra coleção',
            'description': 'A outra descrição'
        }
    ]

    return collections


def get_publisher_mocked() -> list[dict[str, Any]]:
    publishers: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 1,
            'name': 'Suma',
        },
        {
            **default_model_dict,
            'id': 2,
            'name': 'Rocco'
        }
    ]

    return publishers


def get_author_mocked() -> list[dict[str, Any]]:
    languages = get_language_mocked()
    countries = get_country_mocked()

    authors: list[dict[str, Any]] = [
        {
            **default_model_dict,
            'id': 1,
            'name': 'Jack Ryan',
            'language_id': languages[0]['id'],
            'country_id': countries[0]['id'],
        },
        {
            **default_model_dict,
            'id': 2,
            'name': 'Jason Bourne',
            'language_id': languages[1]['id'],
            'country_id': countries[1]['id'],
        },
        {
            **default_model_dict,
            'id': 3,
            'name': 'Frodo Baggins',
            'language_id': languages[0]['id'],
            'country_id': countries[0]['id'],
        }
    ]

    return authors
