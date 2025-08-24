import datetime
import uuid

from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    id: int | None = Field(None, alias="itemId", description="Id of the item")
    owner_id: uuid.UUID = Field(None, alias="ownerId", description="Id of the owner")
    last_status_id: str = Field(None, alias="lastStatusId", description="Id of the last status of the item")
    last_status_date: datetime.date = Field(..., alias="lastStatusDate", description="Date of the last status of the item")
    main_author_id: int = Field(None, alias='mainAuthorId', description='The id of the main author of the item')
    other_authors_id: list[int] = Field(None, alias='otherAuthorsId', description='The ids of other authors of the item')
    title: str = Field(..., alias='title', description='The name of the item')
    subtitle: str = Field(None, alias='subtitle', description='The subtitle of the item')
    title_original: str = Field(None, alias='titleOriginal', description='The original title of the item')
    subtitle_original: str = Field(None, alias='originalSubtitle', description='The original subtitle of the item')
    isbn: str = Field(None, alias='isbn', description='The ISBN of the item')
    isbn10: str = Field(None, alias='isbn10', description='The ISBN 10 of the item')
    type: str = Field(None, alias='itemType', description='The type of the item')  # maybe Id?
    pages: int = Field(0, alias='pages', description='The number of pages of the item')
    volume: int = Field(0, alias='volume', description='The volume of the item')
    edition: int = Field(1, alias='edition', description='The edition of the item')
    publication_date: datetime.date = Field(None, alias='publicationDate', description='The date of the publish')
    original_publication_date: datetime.date = Field(None, alias='originalPublicationDate', description='The date of the publish')
    serie_id: int = Field(0, alias='serieId', description='The id of the serie')
    collection_id: int = Field(0, alias='collectionId', description='The id of the collection')
    publisher_id: int = Field(None, alias='publisherId', description='The publisher of the item')
    format: str = Field(None, alias='itemFormatId', description='The id of the format')
    language_id: str = Field(None, alias='languageId', description='The id of the language')
    cover_price: float = Field(None, alias='coverPrice', description='The price of the item')
    paid_price: float = Field(None, alias='paidPrice', description='The price of the item')
    dimensions: str = Field(None, alias='dimensions', description='The dimensions of the item')
    height: int = Field(None, alias='height', description='The height of the item')
    width: int = Field(None, alias='width', description='The width of the item')
    thickness: int = Field(None, alias='thickness', description='The thickness of the item')
    summary: str = Field(None, alias='summary', description='The summary of the item')
    observation: str = Field(None, alias='observation', description='The observation of the item')

    cover: str = Field('library/item/cover/no_cover.png', alias='cover', description='Cover of the item')


class UpdateItemRequest(CreateItemRequest):
    # Is basically the same as "Create Item", but without default and required = true
    # and id is required
    id: int = Field(..., alias="itemId", description="Id of the item")
    title: str | None = Field(None, alias='title', description='The name of the item')
    last_status_date: datetime.date | None = Field(None, alias="lastStatusDate", description="Date of the last status of the item")
    pages: int | None = Field(None, alias='pages', description='The number of pages of the item')
    volume: int | None = Field(None, alias='volume', description='The volume of the item')
    edition: int | None = Field(None, alias='edition', description='The edition of the item')
    serie_id: int | None = Field(None, alias='serieId', description='The id of the serie')
    collection_id: int | None = Field(None, alias='collectionId', description='The id of the collection')
    cover: str = Field(None, alias='cover', description='Cover of the item')


class GetItemRequest(BaseModel):
    id: int | None = Field(None, ge=1, alias='itemId')
    title: str | None = Field(None, min_length=3, alias='title')
    main_author_id: int | None = Field(None, alias='mainAuthorId')
    type: str | None = Field(None, alias='itemType')

