from pydantic import BaseModel, Field
from rolf_common.schemas import SuccessResponseBase

from schemas.item import AuthorSchema


class CreateAuthorResponse(SuccessResponseBase):
    author: AuthorSchema


class GetAuthorResponse(BaseModel):
    quantity: int = Field(..., description='The quantity of authors fetched')
    authors: list[AuthorSchema] = Field(..., description='The list of authos fetched')
