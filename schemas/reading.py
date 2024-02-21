import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from schemas.item import ItemSchema


class ReadingSchema(BaseModel):
    __repr_name__ = 'Reading'
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The id of the item")
    item: ItemSchema = Field(..., description="The", exclude=True)
    start_at: datetime.date = Field(..., serialization_alias='startAt', description="The date the reading start")
    # finish_at: datetime.date = Field(..., serialization_alias='finishAt', description="The date the reading ends")
    number: int = Field(..., serialization_alias='readingNumber', description="The number of the reading, if it is first, second time, etc")
    is_dropped: bool = Field(..., serialization_alias='isDropped', description='Indicates if the item was dropped')

    def transform(self):
        self.item_title = self.item.title
        return self


class ProgressSchema(BaseModel):
    __repr_name__ = 'Reading Progress'
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingProgressId', description='The identification of the progress entry')
    reading_id: uuid.UUID = Field(..., serialization_alias='readingId', description='The id of the reading')
    date: datetime.date = Field(..., serialization_alias='date', description='The date that the entry was created')
    page: int = Field(..., serialization_alias='page', description='The current page')
    percentage: float = Field(..., serialization_alias='percentage', description='The current percentage')
    rate: Optional[int] = Field(None, serialization_alias='rate', description='The rate for this entry')
    comment: Optional[str] = Field(None, serialization_alias='comment', description='The comment for this entry')
