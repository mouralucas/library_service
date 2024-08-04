import datetime
import uuid
from dataclasses import dataclass
from typing import Optional, Any

from fastapi import Query
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator, root_validator, ValidationError


class CreateReadingRequest(BaseModel):
    owner_id: uuid.UUID = Field(None, alias="ownerId", description='The owner of the reading')
    item_id: int = Field(..., alias='itemId', description="The id of the item")
    start_date: datetime.date = Field(None, alias='startDate', description="The date that the user start reading the item")
    finish_date: datetime.date = Field(None, alias='finishDate', description="The date that the user finish reading the item")
    is_dropped: bool = Field(False, alias='isDropped', description="Indicate if the user has dropped the item")

    @model_validator(mode='before')
    def check_reading_finished(cls, data: dict) -> dict:
        if not data.get('startDate') and not data.get('finishDate'):
            raise ValueError('start or finish date must be specified')

        return data


class GetReadingRequest(BaseModel):
    item_id: int | None = Field(Query(None, description="The id of the item", summary="The id of the item"), alias='itemId')
    reading_id: uuid.UUID | None = Field(Query(None, description="The id of the reading"), alias='readingId')
    get_progress: bool = Field(Query(False, description="If true return all progress associated with each reading"), alias='getProgress')

    @model_validator(mode='before')
    def check_reading_finished(cls, data: dict) -> dict:
        if data.get('page') and data.get('percentage'):
            raise ValueError('only item_id or reading_id must be specified')

        if not data.get('itemId') and not data.get('readingId'):
            raise ValueError('One of item_id or reading_id must be specified')

        return data


class CreateProgressRequest(BaseModel):
    reading_id: uuid.UUID = Field(..., alias='readingId', description='The id of the the reading')
    page: int = Field(0, alias='page', description='The current page in reading')
    percentage: int = Field(0, alias='percentage', description='The current page in reading', gt=0, le=100)
    date: datetime.date = Field(datetime.date.today(), alias='date', description='The date that progress was taken')
    rate: int = Field(None, alias='rate', description='The rate of the reading so far')
    comment: str = Field(None, alias='comment', description='The comments for the reading so far')

    @model_validator(mode='before')
    def check_mutual_exclusion(cls, data: dict) -> dict:
        if data.get('page') and data.get('percentage'):
            raise ValueError('only page or percentage must be specified')

        if not data.get('page') and not data.get('percentage'):
            raise ValueError('page or percentage must be specified')

        return data


class GetProgressRequest(BaseModel):
    reading_id: uuid.UUID = Field(Query(..., alias='readingId', description="The id of the reading"))
    item_id: uuid.UUID | None = Field(Query(None, alias='itemId', description="The id of the item"))
