from typing import Any
from ariadne import MutationType, QueryType
from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.author import CreateAuthorRequest, GetAuthorsRequest
from schemas.request.core import (
    CreateCollectionRequest,
    CreateCountryRequest,
    CreateLanguageRequest,
    CreatePublisherRequest,
    CreateSerieRequest,
    GetStatusRequest,
)
from services.author import AuthorService
from services.core import (
    CollectionService,
    CountryService,
    LanguageService,
    PublisherService,
    SerieService,
    StatusService,
)


@validate_graphql_input(GetAuthorsRequest)
async def get_authors_resolver(_, info, params: GetAuthorsRequest):
    authors = await AuthorService(session=info.context["session"]).get_authors(params)

    return authors


async def create_author_resolver(_, info, author: dict):
    author_ = CreateAuthorRequest.model_validate(author)

    new_author = await AuthorService(session=info.context["session"]).create_author(
        author=author_
    )

    return new_author.model_dump(by_alias=True)


async def get_series_resolver(_, info) -> dict[str, Any]:
    series = await SerieService(session=info.context["session"]).get_series()

    return series


async def create_serie_resolver(_, info, serie):
    serie_ = CreateSerieRequest.model_validate(serie)

    new_serie = await SerieService(session=info.context["session"]).create_serie(
        serie=serie_
    )

    return new_serie.model_dump(by_alias=True)


async def get_collections_resolver(_, info) -> dict[str, Any]:
    response = await CollectionService(
        session=info.context["session"]
    ).get_collections()

    return response


async def create_collection_resolver(_, info, collection):
    collection_ = CreateCollectionRequest.model_validate(collection)

    new_collection = await CollectionService(
        session=info.context["session"]
    ).create_collection(collection=collection_)

    return new_collection.model_dump(by_alias=True)


async def get_publishers_resolver(_, info) -> dict[str, Any]:
    publishers = await PublisherService(
        session=info.context["session"]
    ).get_publishers()

    return publishers


async def create_publisher_resolver(_, info, publisher):
    publisher_ = CreatePublisherRequest.model_validate(publisher)

    new_publisher = await PublisherService(
        session=info.context["session"]
    ).create_publisher(publisher=publisher_)

    return new_publisher.model_dump(by_alias=True)


async def get_languages_resolver(_, info):
    languages = await LanguageService(session=info.context["session"]).get_languages()

    return languages.model_dump(by_alias=True)


async def crate_language_resolver(_, info, language):
    language_ = CreateLanguageRequest.model_validate(language)

    new_language = await LanguageService(
        session=info.context["session"]
    ).create_language(language=language_)

    return new_language.model_dump(by_alias=True)


async def get_countries_resolver(_, info):
    countries = await CountryService(session=info.context["session"]).get_countries()

    return countries.model_dump(by_alias=True)


async def create_country_resolver(_, info, country):
    country_ = CreateCountryRequest.model_validate(country)

    new_country = await CountryService(session=info.context["session"]).create_country(
        country=country_
    )

    return new_country.model_dump(by_alias=True)


@validate_graphql_input(GetStatusRequest)
async def get_status_resolver(_, info, params: GetStatusRequest):
    statusses = await StatusService(
        session=info.context["session"], user=info.context["user"]
    ).get_status(params=params)

    return statusses


def bind_core_resolvers(query: QueryType, mutation: MutationType):
    query.set_field("getAuthors", resolver=get_authors_resolver)
    query.set_field("getSeries", resolver=get_series_resolver)
    query.set_field("getCollections", resolver=get_collections_resolver)
    query.set_field("getPublishers", resolver=get_publishers_resolver)
    query.set_field("getLanguages", resolver=get_languages_resolver)
    query.set_field("getCountries", resolver=get_countries_resolver)
    query.set_field("getStatus", resolver=get_status_resolver)

    mutation.set_field("createAuthor", resolver=create_author_resolver)
    mutation.set_field("createSerie", resolver=create_author_resolver)
    mutation.set_field("createCollection", resolver=create_collection_resolver)
    mutation.set_field("createLanguage", resolver=crate_language_resolver)
    mutation.set_field("createCountry", resolver=create_country_resolver)
