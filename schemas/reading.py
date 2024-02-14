from typing import Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel, Field, ConfigDict
import uuid
import datetime

class ReadingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
    # TODO: add other fields


class ProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingProgressId', description='The identification of the progress entry')
    reading_id: uuid.UUID = Field(..., serialization_alias='readingId', description='The id of the reading')
    date: datetime.date = Field(..., serialization_alias='date', description='The date that the entry was created')
    page: int = Field(..., serialization_alias='page', description='The current page')
    percentage: float = Field(..., serialization_alias='percentage', description='The current percentage')
    rate: Optional[int] = Field(None, serialization_alias='rate', description='The rate for this entry')
    comment: Optional[str] = Field(None, serialization_alias='comment', description='The comment for this entry')
    # TODO: add other fields
