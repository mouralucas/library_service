import uuid
from datetime import datetime, date
from fastapi import Query
from pydantic import BaseModel, Field, model_validator, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel
from services.utils.datetime import utc_timestamp, current_date


class CreateReadingRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    owner_id: uuid.UUID | None = Field(None, alias="ownerId", description='The owner of the reading')
    item_id: int = Field(..., alias='itemId', description="The id of the item")
    start_date: date = Field(default_factory=current_date, alias='startDate', description="The date that the user start reading the item")
    finish_date: date | None = Field(None, alias='finishDate', description="The date that the user finish reading the item")
    is_dropped: bool = Field(False, alias='isDropped', description="Indicate if the user has dropped the item")


class GetReadingRequest(BaseModel):
    item_id: int | None = Field(Query(None, description="The id of the item", summary="The id of the item"), alias='itemId')
    reading_id: uuid.UUID | None = Field(Query(None, description="The id of the reading"), alias='readingId')
    get_progress: bool = Field(Query(False, description="If true return all progress associated with each reading"), alias='getProgress')

    # TODO: Change validation to 'after'
    @model_validator(mode='before')
    def check_reading_finished(cls, data: dict) -> dict:
        if data.get('page') and data.get('percentage'):
            raise ValueError('only item_id or reading_id must be specified')

        if not data.get('itemId') and not data.get('readingId'):
            raise ValueError('One of item_id or reading_id must be specified')

        return data


class CreateProgressRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    reading_id: uuid.UUID = Field(..., alias='readingId', description='The id of the the reading')
    page: int = Field(0, alias='page', description='The current page in reading')
    percentage: int = Field(0, alias='percentage', description='The current page in reading', gt=0, le=100)
    progressDate: date = Field(default_factory=date.today, alias='progressDate', description='The date that progress was taken')
    rate: int | None = Field(None, alias='rate', description='The rate of the reading so far')
    comment: str | None = Field(None, alias='comment', description='The comments for the reading so far')

    # TODO: Change validation to 'after'
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


class GetReadingStatsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    item_id: int = Field(..., description="The id of the item")