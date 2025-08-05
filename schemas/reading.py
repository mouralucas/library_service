import uuid
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict

from schemas.core import StatusSchema
from schemas.item import ItemSchema


class ProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingProgressId', description='The identification of the progress entry')
    reading_id: uuid.UUID = Field(..., serialization_alias='readingId', description='The id of the reading')
    progressDate: date = Field(..., serialization_alias='date', description='The date that the entry was created')
    page: int = Field(..., serialization_alias='page', description='The current page')
    percentage: float = Field(..., serialization_alias='percentage', description='The current percentage')
    rate: int | None = Field(None, serialization_alias='rate', description='The rate for this entry')
    comment: str | None = Field(None, serialization_alias='comment', description='The comment for this entry')


class ReadingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item: ItemSchema = Field(..., description="The item of the reading")
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The title of the item")
    start_date: date = Field(..., serialization_alias='startDate', description="The date the reading start")
    finish_date: date | None = Field(None, serialization_alias='finishDate', description="The date the reading ends")
    number: int = Field(..., serialization_alias='readingNumber', description="The number of the reading, if it is first, second time, etc")
    active: bool = Field(..., serialization_alias='active', description='If false reading could be finished or dropped, if true is reading now, check status')
    status: StatusSchema = Field(..., description='The status of the reading')
    status_id: str = Field(..., serialization_alias='statusId', description="The id of the status")
    status_name: str | None = Field(None, description='The name of the status')
    progress: list[ProgressSchema] | None = Field(None, serialization_alias='progress', description="The current progress of the reading")

    # TODO: change transform to a validate_model after
    def transform(self):
        self.item_title = self.item.title
        self.status_name = self.status.name
        # Add transformation as needed
        return self

class ReadingStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    readings_count: int = Field(..., serialization_alias='readingsCount', description='The total number of readings')
    last_reading_date: date | None = Field(None, serialization_alias='lastReadingDate', description='The date of the last reading')
    current_page: int | None = Field(None, serialization_alias='currentPage', description='The current page of the reading')
    current_percentage: float | None = Field(None, serialization_alias='currentPercentage', description='The current percentage of the reading')
    