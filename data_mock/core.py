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