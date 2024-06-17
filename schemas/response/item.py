from rolf_common.schemas import SuccessResponseBase
from schemas.item import ItemSchema


class CreateItemResponse(SuccessResponseBase):
    item: ItemSchema


class GetItemResponse(SuccessResponseBase):
    quantity: int
    items: list[ItemSchema]
