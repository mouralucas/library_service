from schemas.base import SuccessResponseBase
from schemas.item import ItemSchema


class GetItemResponse(SuccessResponseBase):
    quantity: int
    items: list[ItemSchema]
