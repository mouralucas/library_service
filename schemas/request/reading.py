import uuid
from dataclasses import dataclass
from typing import Optional, Any

from fastapi import Query
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator


class CreateReadingRequest(BaseModel):
    item_id: int = Field(..., alias='itemId', description="The id of the item")
    start_at: str = Field(..., alias='startAt', description="The date that the user start reading the item")
    finish_at: str = Field(None, alias='finishAt', description="The date that the user finish reading the item")
    is_dropped: bool = Field(False, alias='isDropped', description="Indicate if the user has dropped the item")


@dataclass
class GetReadingRequest:
    item_id: int = Query(..., alias='itemId', description="The id of the item", summary="The id of the item")


class CreateProgressRequest(BaseModel):
    reading_id: uuid.UUID = Field(..., alias='readingId', description='The id of the the reading')
    page: int = Field(None, alias='page', description='The current page in reading')
    percentage: int = Field(None, alias='percentage', description='The current page in reading')
    rate: int = Field(None, alias='rate', description='The rate of the reading so far')
    comment: str = Field(None, alias='comment', description='The comments for the reading so far')

    @model_validator(mode='before')
    def check_mutual_exclusion(cls, data: dict) -> dict:
        if data.get('page') and data.get('percentage'):
            raise ValueError('only page or percentage must be passed')

        if not data.get('page') and not data.get('percentage'):
            raise ValueError('page or percentage must be passed')

        return data


@dataclass
class GetProgressRequest:
    reading_id: uuid.UUID = Query(..., alias='readingId', description="The id of the reading")
