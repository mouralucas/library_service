import uuid

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict


class CreateReadingRequest(BaseModel):
    item_id: int = Field(..., alias='itemId', description="The id of the item")
    start_at: str = Field(..., alias='startAt', description="The date that the user start reading the item")
    finish_at: str = Field(None, alias='finishAt', description="The date that the user finish reading the item")
    is_dropped: bool = Field(False, alias='isDropped', description="Indicate if the user has dropped the item")


class GetReadingRequest(BaseModel):
    item_id: int = Query(..., alias='itemId', description="The id of the item", summary="The id of the item")


class GetReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., serialization_alias='readingId', description="The id of the reading")
    item_id: int = Field(..., serialization_alias='itemId', description="The id of the item")
