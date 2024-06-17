from rolf_common.schemas import SuccessResponseBase
from schemas.item import AuthorSchema


class CreateAuthorResponse(SuccessResponseBase):
    author: AuthorSchema


class GetAuthorResponse(SuccessResponseBase):
    quantity: int
    authors: list[AuthorSchema]
