import datetime
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict


class ItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias='itemId', description='The id of the item')
    # main author
    title: str = Field(..., description="The title of the item")
    subtitle: str | None = Field(None, description='The subtitle of the item, if exists')
    original_title: str = Field(None, serialization_alias='originalTitle', description="The original title of the item")
    original_subtitle: str = Field(None, serialization_alias='originalSubtitle', description="The original title of the item")
    isbn: str = Field(None, description='ISBN number of the item', alias='isbn_formatted')
    isbn10: str = Field(None, description='ISBN 10 number of the item')
    # item type
    pages: int = Field(None, description='The number of pages of the item')
    volume: int = Field(0, description='The volume of the item')
    edition: int = Field(1, description='The edition of the item')
    published_at: datetime.date = Field(None, serialization_alias='publishedAt', description='The date of publication of the item')
    published_original_at: datetime.date = Field(None, serialization='publishedOriginalAt', description='The original date of publication')
    # serie
    # collection
    # publisher
    # format
    # language
    cover_price: float = Field(None, serialization_alias='coverPrice', description='The cover price of the item')
    paid_price: float = Field(None, serialization_alias='paidPrice', description='The item paid price')


class GetItemRequest:
    itemId: int = Query(..., title='Id do item', description="Identificação única do item na base de dados")


@dataclass
class Request:
    scalar_parameter: int = Query(None)
    list_parameter: list[int] = Query(None)


class GetItemResponse(BaseModel):
    itemId: int = Field(..., title='Id do item', description="")
    itemName: str = Field(..., title='Nome do item')
