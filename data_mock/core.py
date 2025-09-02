from typing import Any

from rolf_common.util.datetime import get_timestamp_aware

default_model_dict = {"created_at": get_timestamp_aware(), "active": True}


def get_item_status_mock() -> list[dict[str, Any]]:
    item_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": "owned",
            "name": "Na estante",
            "type": "ITEM.STATUS",
        },
        {
            **default_model_dict,
            "id": "bought",
            "name": "Comprado",
            "type": "ITEM.STATUS",
        },
        {
            **default_model_dict,
            "id": "sold",
            "name": "Vendido",
            "type": "ITEM.STATUS",
        },
        {
            **default_model_dict,
            "id": "wished",
            "name": "Desejado",
            "type": "ITEM.STATUS",
        },
    ]

    return item_status


def get_reading_status_mock() -> list[dict[str, Any]]:
    reading_status: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": "reading",
            "name": "Lendo",
            "type": "READING.STATUS",
        },
        {
            **default_model_dict,
            "id": "read",
            "name": "Lido",
            "type": "READING.STATUS",
        },
    ]

    return reading_status


def get_language_mock() -> list[dict[str, Any]]:
    languages: list[dict[str, Any]] = [
        {**default_model_dict, "id": "EN", "name": "Inglês", "code": "EN"},
        {**default_model_dict, "id": "PT", "name": "Português", "code": "PT"},
        {**default_model_dict, "id": "DE", "name": "Alemão", "code": "DE"},
        {**default_model_dict, "id": "JP", "name": "Japan", "code": "JP"},
    ]

    return languages


def get_country_mock() -> list[dict[str, Any]]:
    countries: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": "BR",
            "name": "Brasil",
            "continent": "SA",
        },
        {
            **default_model_dict,
            "id": "DE",
            "name": "Alemanha",
            "continent": "EU",
        },
        {
            **default_model_dict,
            "id": "AU",
            "name": "Austrália",
            "continent": "OC",
        },
        {
            **default_model_dict,
            "id": "US",
            "name": "Estados Unidos",
            "continent": "NA",
        },
        {
            **default_model_dict,
            "id": "JP",
            "name": "Japão",
            "continent": "AS",
        },
    ]

    return countries


def get_serie_mock() -> list[dict[str, Any]]:
    series: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": 0,
            "name": "Volume único",
            "description": "Não pertence a nenhuma série específica",
        },
        {
            **default_model_dict,
            "id": 1,
            "name": "A torre negra",
            "description": "A Torre Negra, no original, The Dark Tower, "
            "é uma série literária do escritor americano Stephen King. "
            "Misturando alta fantasia, faroeste, ficção científica e terror numa narrativa que "
            'forma um mosaico da cultura popular contemporânea, o enredo segue um "pistoleiro" '
            "e sua busca em direção a uma torre, a Torre Negra, cuja natureza é tanto física quanto metafórica",
        },
        {
            **default_model_dict,
            "id": 2,
            "name": "Neon Genesis Evangelion",
            "description": "O enredo de Evangelion se passa em 2015, em um mundo que acabara de ser reconstruído após a dizimação "
            "de metade da humanidade na catástrofe que ficou conhecida como “Segundo Impacto”. O Japão ganha uma capital "
            "provisória, a Tokyo-2, cujo Governo promove a construção da futura capital denominada Tokyo-3. "
            "Mas a construção da nova metrópole serve apenas de fachada para erguer uma cidade-fortaleza com tecnologia "
            "altamente avançada para resistir à ofensiva dos Anjos, monstruosos seres, cujo ataque já havia sido previsto "
            "pela humanidade. A organização especial paramilitar, denominada NERV, foi incumbida da missão de combater tais "
            "ameaças usando mechas gigantes chamados de Evas, que são pilotados por jovens rigorosamente selecionados. "
            "Um deles é Shinji Ikari, um tímido adolescente. Na realidade, há mais de dez anos ele foi abandonado pelo pai, "
            "Gendo Ikari, atual comandante supremo da NERV. Aos 14 anos, Shinji é chamado por ele para pilotar o incrível EVA-01, "
            "a última esperança da humanidade na batalha contra os Anjos. Assim dá-se início a uma aventura inigualável em que "
            "ficção científica se mistura aos sentimentos mais complexos e profundos do ser humano.",
        },
    ]

    return series


def get_collection_mock() -> list[dict[str, Any]]:
    collections: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": 0,
            "name": "Não consta",
            "description": "Não pertence a nenhuma coleção específica",
        },
        {
            **default_model_dict,
            "id": 1,
            "name": "Biblioteca Stephen King",
            "description": "Coleção em capa dura dos clássicos de Stephen King",
        },
        {
            **default_model_dict,
            "id": 2,
            "name": "Evangelion Colecionador",
            "description": "Edição de colecionador, em 7 volumes",
        },
    ]

    return collections


def get_publisher_mock() -> list[dict[str, Any]]:
    publishers: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": 1,
            "name": "Suma",
        },
        {
            **default_model_dict,
            "id": 2,
            "name": "Rocco",
        },
        {
            **default_model_dict,
            "id": 3,
            "name": "JBC",
        },
        {
            **default_model_dict,
            "id": 4,
            "name": "Intrínseca",
        },
    ]

    return publishers


def get_author_mock() -> list[dict[str, Any]]:
    languages = get_language_mock()
    countries = get_country_mock()

    authors: list[dict[str, Any]] = [
        {
            **default_model_dict,
            "id": 1,
            "name": "Stephen King",
            "language_id": languages[0]["id"],
            "country_id": countries[3]["id"],
        },
        {
            **default_model_dict,
            "id": 2,
            "name": "Yoshiyuki Sadamoto",
            "language_id": languages[3]["id"],
            "country_id": countries[4]["id"],
        },
        {
            **default_model_dict,
            "id": 3,
            "name": "Anne Rice",
            "language_id": languages[0]["id"],
            "country_id": countries[3]["id"],
        },
        {
            **default_model_dict,
            "id": 4,
            "name": "Neil Gaiman",
            "language_id": languages[0]["id"],
            "country_id": countries[3]["id"],
        },
    ]

    return authors
