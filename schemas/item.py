import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.core import LanguageSchema, StatusSchema, AuthorSchema, SerieSchema, CollectionSchema, PublisherSchema


class ItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias='itemId', description='The id of the item')
    main_author_id: int = Field(..., serialization_alias='mainAuthorId', description='The id of the main author')
    main_author: AuthorSchema = Field(..., serialization_alias='mainAuthor', description='The author of the item')
    title: str = Field(..., description="The title of the item")
    subtitle: str | None = Field(None, description='The subtitle of the item, if exists')
    original_title: str = Field(None, serialization_alias='originalTitle', description="The original title of the item")
    original_subtitle: str = Field(None, serialization_alias='originalSubtitle', description="The original title of the item")
    isbn: str | None = Field(None, description='ISBN number of the item', alias='isbn_formatted')
    isbn10: str | None = Field(None, description='ISBN 10 number of the item')
    type: str | None = Field(None, serialization_alias='itemType', description='The type of item')
    pages: int | None = Field(None, description='The number of pages of the item')
    volume: int | None = Field(0, description='The volume of the item')
    edition: int | None = Field(1, description='The edition of the item')
    published_at: datetime.date | None = Field(None, serialization_alias='publishedAt', description='The date of publication of the item')
    published_original_at: datetime.date | None = Field(None, serialization_alias='publishedOriginalAt', description='The original date of publication')
    serie_id: int = Field(..., serialization_alias='serieId', description='The id of the serie')
    serie: SerieSchema | None = Field(None, serialization_alias='serie', description='The series object of the item')
    collection_id: int = Field(..., serialization_alias='collectionId', description='The id of the collection')
    collection: CollectionSchema | None = Field(None, description='The collection object of the item')
    publisher_id: int | None = Field(None, serialization_alias='publisherId', description='The id of the publisher')
    publisher: PublisherSchema | None = Field(None, description='The publisher of the item')
    format: str | None = Field(None, serialization_alias='itemFormat', description='The format of the item')
    language: LanguageSchema | None = Field(None, description='The language of the item')
    cover_price: float | None = Field(None, serialization_alias='coverPrice', description='The cover price of the item')
    paid_price: float | None = Field(None, serialization_alias='paidPrice', description='The item paid price')

    last_status_id: str = Field(..., serialization_alias='lastStatusId', description='The id of the last status of the item')
    last_status: StatusSchema | None = Field(None, serialization_alias='lastStatus')
    last_status_date: datetime.date | None = Field(None, serialization_alias='lastStatusDate')