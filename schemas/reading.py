import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from schemas.item import ItemSchema


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


class ReadingSchema(BaseModel):
    __repr_name__ = 'Reading'
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item: ItemSchema = Field(..., description="The", exclude=True)
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
    item_title: str = Field(None, serialization_alias='itemTitle', description="The title of the item")
    start_date: datetime.date = Field(..., serialization_alias='startDate', description="The date the reading start")
    finish_date: datetime.date | None = Field(None, serialization_alias='finishDate', description="The date the reading ends")
    number: int = Field(..., serialization_alias='readingNumber', description="The number of the reading, if it is first, second time, etc")
    active: bool = Field(..., serialization_alias='active', description='If false reading could be finished or dropped, if true is reading now, check status')
    progress: list[ProgressSchema] | None = Field(None, serialization_alias='progress', description="The current progress of the reading")

    def transform(self):
        self.item_title = self.item.title
        # Add transformation as needed
        return self
