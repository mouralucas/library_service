import datetime
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from schemas.core import LanguageSchema, StatusSchema


class SerieSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class CollectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PublisherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_full: str


class ItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias='itemId', description='The id of the item')
    main_author: AuthorSchema = Field(..., description='The author of the item')
    title: str = Field(..., description="The title of the item")
    subtitle: str | None = Field(None, description='The subtitle of the item, if exists')
    original_title: str = Field(None, serialization_alias='originalTitle', description="The original title of the item")
    original_subtitle: str = Field(None, serialization_alias='originalSubtitle', description="The original title of the item")
    isbn: str | None = Field(None, description='ISBN number of the item', alias='isbn_formatted')
    isbn10: str | None = Field(None, description='ISBN 10 number of the item')
    # item type
    pages: int | None = Field(None, description='The number of pages of the item')
    volume: int | None = Field(0, description='The volume of the item')
    edition: int | None = Field(1, description='The edition of the item')
    published_at: datetime.date | None = Field(None, serialization_alias='publishedAt', description='The date of publication of the item')
    published_original_at: datetime.date | None = Field(None, serialization_alias='publishedOriginalAt', description='The original date of publication')
    serie_id: int | None = Field(None, description='The id of the serie')
    serie: SerieSchema | None = Field(None, serialization_alias='serie', description='The series object of the item')
    collection: CollectionSchema | None = Field(None, description='The collection object of the item')
    publisher: PublisherSchema | None = Field(None, description='The publisher of the item')
    # format
    language: LanguageSchema | None = Field(None, description='The language of the item')
    cover_price: float | None = Field(None, serialization_alias='coverPrice', description='The cover price of the item')
    paid_price: float | None = Field(None, serialization_alias='paidPrice', description='The item paid price')

    last_status: StatusSchema | None = Field(None, serialization_alias='lastStatus')
    last_status_date: datetime.date | None = Field(None, serialization_alias='lastStatusDate')


class GetItemResponse(BaseModel):
    itemId: int = Field(..., title='Id do item', description="")
    itemName: str = Field(..., title='Nome do item')
