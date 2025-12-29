import uuid

from ariadne import (
    MutationType,
    QueryType,
    graphql,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.explorer import ExplorerGraphiQL
from fastapi import APIRouter, Depends, Request
from rolf_common.schemas.auth import RequiredUser
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, JSONResponse

from backend.database import get_session
from backend.graphql_scalars import date_scalar, datetime_scalar
from resolvers.item_v2 import bind_items_resolvers_v2

router = APIRouter(tags=["GraphQL"], prefix="/v2/graphql/library")

type_defs = load_schema_from_path("schemas/graphql/")

query = QueryType()
mutation = MutationType()

# Associate the resolvers
bind_items_resolvers_v2(query, mutation)

schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    date_scalar,
    datetime_scalar,
    snake_case_fallback_resolvers,
)


@router.post("", description="The V2 maps all GraphQL endpoint")
async def graphql_server(
    request: Request,
    # user: RequiredUser = Security(get_user),
    session: AsyncSession = Depends(get_session),
):
    user = RequiredUser(user_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"))
    data = await request.json()
    value = {"request": request, "session": session, "user": user}
    success, result = await graphql(schema, data, context_value=value, debug=True)

    status_code = 200 if success else 400
    return JSONResponse(result, status_code=status_code)


playground_html = ExplorerGraphiQL().html(None)


@router.get("", description="The GraphQL playground page")
async def graphql_playground():
    return HTMLResponse(playground_html)
