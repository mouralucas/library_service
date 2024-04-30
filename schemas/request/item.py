from dataclasses import dataclass
import datetime
from fastapi import Query
from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    id: int = Field(None, alias="itemId", description="Id of the item")
    last_status_id: str = Field(None, alias="lastStatusId", description="Id of the last status of the item")
    last_status_at: datetime.date = Field(None, alias="lastStatusDate", description="Date of the last status of the item")
    main_author_id: int = Field(None, alias='mainAuthorId', description='The id of the main author of the item')
    # list_authors_id
    title: int = Field(..., alias='itemTitle', description='The name of the item')
    subtitle: str = Field(None, alias='subtitle', description='The subtitle of the item')
    title_original: str = Field(None, alias='originalTitle', description='The original title of the item')
    subtitle_original: str = Field(None, alias='originalSubtitle', description='The original subtitle of the item')
    isbn: str = Field(None, alias='isbn', description='The ISBN of the item')
    isbn10: str = Field(None, alias='isbn10', description='The ISBN 10 of the item')
    type: str = Field(None, alias='type', description='The type of the item')  # maybe Id?
    pages: int = Field(0, alias='pages', description='The number of pages of the item')
    volume: int = Field(0, alias='volume', description='The volume of the item')
    edition: int = Field(1, alias='edition', description='The edition of the item')
    published_at: datetime.date = Field(None, alias='publishDate', description='The date of the publish')
    published_original_at: datetime.date = Field(None, alias='originalPublishDate', description='The date of the publish')
    serie_id: int = Field(None, alias='serieId', description='The id of the serie')
    collection_id: int = Field(None, alias='collectionId', description='The id of the collection')
    publisher_id: int = Field(None, alias='publisherId', description='The publisher of the item')
    format: str = Field(None, alias='formatId', description='The id of the format')
    language_id: int = Field(None, alias='languageId', description='The id of the language')
    cover_price: float = Field(None, alias='coverPrice', description='The price of the item')
    paid_price: float = Field(None, alias='paidPrice', description='The price of the item')
    dimensions: str = Field(None, alias='dimensions', description='The dimensions of the item')
    height: int = Field(None, alias='height', description='The height of the item')
    width: int = Field(None, alias='width', description='The width of the item')
    thickness: int = Field(None, alias='thickness', description='The thickness of the item')
    summary: str = Field(None, alias='summary', description='The summary of the item')
    observation: str = Field(None, alias='observation', description='The observation of the item')

    cover: str = Field('library/item/cover/no_cover.png', alias='cover', description='Cover of the item')


@dataclass
class GetItemRequest:
    itemId: int = Query(None, title='Id do item', description="Identificação única do item na base de dados")
