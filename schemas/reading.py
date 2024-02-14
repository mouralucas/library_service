from fastapi.openapi.models import Schema
from pydantic import BaseModel, Field, ConfigDict
import uuid


class ReadingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
    # TODO: add other fields


class ProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingProgressId', description='The identification of the progress entry')
    reading_id: int = Field(..., serialization_alias='readingId', description='The id of the reading')
    # TODO: add other fields
