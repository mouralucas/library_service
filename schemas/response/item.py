from pydantic import Field
from rolf_common.schemas import SuccessResponseBase
from rolf_common.schemas.base import DefaultModel

from schemas.item import ItemSchema


class CreateItemResponse(DefaultModel):
    item: ItemSchema = Field(..., description='The item created')


class GetItemResponse(DefaultModel):
    quantity: int = Field(..., description='Quantity of items')
    items: list[ItemSchema] | None = Field(..., description='List of the items')
