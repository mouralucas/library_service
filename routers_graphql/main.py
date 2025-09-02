from ariadne import (
    MutationType,
    QueryType,
    graphql,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.explorer import ExplorerGraphiQL
from fastapi import APIRouter, Depends, Request, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, JSONResponse

from backend.database import get_session
from resolvers.core import bind_core_resolvers
from resolvers.item import bind_item_resolvers
from resolvers.reading import bind_reading_resolvers

router = APIRouter(tags=["GraphQL"], prefix="/graphql/library")

type_defs = (
    load_schema_from_path("schemas_graphql/base.graphql")
    + load_schema_from_path("schemas_graphql/core.graphql")
    + load_schema_from_path("schemas_graphql/reading.graphql")
    + load_schema_from_path("schemas_graphql/item.graphql")
)

query = QueryType()
mutation = MutationType()

# Associa os resolvers
bind_core_resolvers(query, mutation)
bind_item_resolvers(query, mutation)
bind_reading_resolvers(query, mutation)


schema = make_executable_schema(type_defs, query, mutation)


@router.post("", description="The V2 maps all GraphQL endpoint")
async def graphql_server(
    request: Request,
    user: RequiredUser = Security(get_user),
    session: AsyncSession = Depends(get_session),
):
    # user = RequiredUser(user_id=uuid.uuid4())
    data = await request.json()
    value = {"request": request, "session": session, "user": user}
    success, result = await graphql(schema, data, context_value=value, debug=True)

    status_code = 200 if success else 400
    return JSONResponse(result, status_code=status_code)


playground_html = ExplorerGraphiQL().html(None)


@router.get("", description="The GraphQL playground page")
async def graphql_playground():
    return HTMLResponse(playground_html)
