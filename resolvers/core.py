from ariadne import MutationType, QueryType

from schemas.request.author import CreateAuthorRequest, GetAuthorsRequest
from services.author import AuthorService


async def get_authors_resolver(_, info, params):
    params_ = GetAuthorsRequest.model_validate(params)

    authors = await AuthorService(session=info.context["session"]).get_author(params_)

    return authors.model_dump(by_alias=True)


async def create_author_resolver(_, info, author: dict):
    author_ = CreateAuthorRequest.model_validate(author)

    new_author = await AuthorService(session=info.context["session"]).create_author(author=author_)

    return new_author.model_dump(by_alias=True)

def bind_core_resolvers(query: QueryType, mutation: MutationType):
    query.set_field("getAuthors", get_authors_resolver)

    mutation.set_field("createAuthor", create_author_resolver)
