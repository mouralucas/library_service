

from schemas.request.author import GetAuthorsRequest
from services.author import AuthorService


async def get_authors_resolver(_, info, params):
    params_ = GetAuthorsRequest.model_validate(params)

    authors = await AuthorService(session=info.context["session"]).get_author()
    
    return authors.model_dump(by_alias=True)


def bind_core_resolvers(query, mutation):
    query.set_field("getAuthors", get_authors_resolver)