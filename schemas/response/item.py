from pydantic import Field
from rolf_common.schemas import SuccessResponseBase
from schemas.item import ItemSchema


class CreateItemResponse(SuccessResponseBase):
    item: ItemSchema = Field(..., description='The item created')


class GetItemResponse(SuccessResponseBase):
    quantity: int = Field(..., description='Quantity of items')
    items: list[ItemSchema] | None = Field(..., description='List of the items')
