from fastapi import APIRouter
from ariadne import load_schema_from_path, QueryType, MutationType

router = APIRouter(tags=['Reading GraphQL'], prefix='/v2/reading')


type_defs = (
    load_schema_from_path('schemas_graphql/reading.graphql')
)

query = QueryType()
mutation = MutationType()