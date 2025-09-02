import datetime

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from schemas.core import (
    AuthorSchema,
    CollectionSchema,
    LanguageSchema,
    PublisherSchema,
    SerieSchema,
    StatusSchema,
)


class ItemSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: int = Field(..., serialization_alias="itemId", description="The id of the item")
    main_author_id: int = Field(..., description="The id of the main author")
    main_author_name: str | None = Field(
        None, description="The name of the main author"
    )
    main_author: AuthorSchema | None = Field(None, description="The author of the item")
    title: str = Field(..., description="The title of the item")
    subtitle: str | None = Field(
        None, description="The subtitle of the item, if exists"
    )
    title_original: str | None = Field(
        None, description="The original title of the item"
    )
    subtitle_original: str | None = Field(
        None, description="The original title of the item"
    )
    isbn: str | None = Field(None, description="ISBN number of the item")
    isbn10: str | None = Field(None, description="ISBN 10 number of the item")
    type: str | None = Field(
        None, serialization_alias="itemType", description="The type of item"
    )
    pages: int | None = Field(None, description="The number of pages of the item")
    volume: int | None = Field(0, description="The volume of the item")
    edition: int | None = Field(1, description="The edition of the item")
    publication_date: datetime.date | None = Field(
        None, description="The date of publication of the item"
    )
    original_publication_date: datetime.date | None = Field(
        None, description="The original date of publication"
    )
    serie_id: int = Field(..., description="The id of the serie")
    serie_name: str | None = Field(None, description="The name of the serie")
    serie: SerieSchema | None = Field(None, description="The series object of the item")
    collection_id: int = Field(..., description="The id of the collection")
    collection_name: str | None = Field(None, description="The name of the collection")
    collection: CollectionSchema | None = Field(
        None, description="The collection object of the item"
    )
    publisher_id: int | None = Field(None, description="The id of the publisher")
    publisher_name: str | None = Field(None, description="The name of the publisher")
    publisher: PublisherSchema | None = Field(
        None, description="The publisher of the item"
    )
    format: str | None = Field(
        None, serialization_alias="formatId", description="The format of the item"
    )
    language_id: str | None = Field(None, description="The id of the language")
    language: LanguageSchema | None = Field(
        None, description="The language of the item"
    )
    cover_price: float | None = Field(None, description="The cover price of the item")
    paid_price: float | None = Field(None, description="The item paid price")
    dimensions: str | None = Field(None, description="The item dimensions")
    height: float | None = Field(None, description="The height of the item")
    width: float | None = Field(None, description="The width of the item")
    thickness: float | None = Field(None, description="The thickness of the item")
    observation: str | None = Field(None, description="The observation of the item")
    last_status_id: str = Field(
        ..., description="The id of the last status of the item"
    )
    last_status_name: str | None = Field(
        None, description="The name of the last status"
    )
    last_status: StatusSchema | None = Field(
        None, description="The last status of the item"
    )
    last_status_date: datetime.date | None = Field(
        None, description="The date of the last status of the item"
    )

    summary: str | None = Field(None, description="The summary of the item")

    def transform(self, item):
        pass
