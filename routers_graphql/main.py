from ariadne import load_schema_from_path, QueryType, MutationType, make_executable_schema, graphql
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerPlayground, ExplorerGraphiQL
from fastapi import APIRouter, Request, Depends, Security
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, HTMLResponse

from backend.database import get_session
from resolvers.item import bind_item_resolvers
from resolvers.reading import bind_reading_resolvers
import uuid

router = APIRouter(tags=["GraphQL"], prefix='/v2/item')

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

@router.post('', description='The V2 maps all GraphQL endpoint')
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

@router.get('', description='The GraphQL playground page')
async def graphql_playground():
    # TODO: edit to render GraphiQL playground
    return HTMLResponse(playground_html)
