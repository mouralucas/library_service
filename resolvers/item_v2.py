from ariadne import MutationType, QueryType
import uuid
from graphql import GraphQLResolveInfo
from rolf_common.util.graphql_input_validation import validate_graphql_input

from schemas.request.item_v2 import GetItemsV2Request
from services.item_v2 import ItemServiceV2


@validate_graphql_input(GetItemsV2Request)
async def get_iteme_editions_resolver(_, info: GraphQLResolveInfo, params: GetItemsV2Request):
    editions = await ItemServiceV2(session=info.context["session"]).get_editions(
        owner_id=uuid.UUID("4515f507-918b-445f-8a56-b9170f0d48e9")
    )
    
    return editions


def bind_items_resolvers_v2(query: QueryType, mutation: MutationType):
    query.set_field("getItemEditions", resolver=get_iteme_editions_resolver)
