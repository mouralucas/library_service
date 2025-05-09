from ariadne import load_schema_from_path, QueryType, MutationType, make_executable_schema, graphql_sync
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerPlayground
from fastapi import APIRouter, Request, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, HTMLResponse

from backend.database import get_session
from resolvers.item import bind_item_resolvers
from resolvers.reading import bind_reading_resolvers

router = APIRouter(tags=["GraphQL"])

type_defs = (
        load_schema_from_path("schemas_graphql/base.graphql") +
        load_schema_from_path("schemas_graphql/reading.graphql") +
        load_schema_from_path("schemas_graphql/item.graphql")
)

query = QueryType()
mutation = MutationType()

# Associa os resolvers
bind_reading_resolvers(query, mutation)
bind_item_resolvers(query, mutation)

schema = make_executable_schema(type_defs, query, mutation)


@router.post('/graphql')
async def graphql_server(
        request: Request,
        # user: RequiredUser = Security(get_user),
        session: AsyncSession = Depends(get_session),
):
    user = None
    data = await request.json()
    value = {"request": request, "session": session, "user": user}
    success, result = graphql_sync(schema, data, context_value=value, debug=True)
    status_code = 200 if success else 400
    return JSONResponse(result, status_code=status_code)

playground_html = ExplorerPlayground().html(None)

@router.get("/graphql")
async def graphql_playground():
    return HTMLResponse(playground_html)
