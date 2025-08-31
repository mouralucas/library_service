import uuid
from datetime import date
from typing import Literal

from fastapi import Query
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from services.utils.datetime import current_date


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

    @model_validator(mode='after')
    def check_reading_finished(self) -> 'GetReadingRequest':
        if self.item_id and self.reading_id:
            raise ValueError('only item_id or reading_id must be specified')

        return self


class CreateProgressRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    reading_id: uuid.UUID = Field(..., alias='readingId', description='The id of the the reading')
    page: int = Field(0, alias='page', description='The current page in reading')
    percentage: int = Field(0, alias='percentage', description='The current page in reading', gt=0, le=100)
    progress_date: date = Field(default_factory=date.today, alias='progressDate', description='The date that progress was taken')
    rate: int | None = Field(None, alias='rate', description='The rate of the reading so far')
    comment: str | None = Field(None, alias='comment', description='The comments for the reading so far')

    @model_validator(mode='after')
    def check_percentage_value(self) -> 'CreateProgressRequest':
        if self.page and self.percentage:
            raise ValueError('only page or percentage must be specified')

        if not self.page and not self.percentage:
            raise ValueError('page or percentage must be specified')

        return self


class CreateProgressRequestV2(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    reading_id: uuid.UUID = Field(..., description='The id of the the reading')
    progress_type: Literal['percentage', 'page'] = Field(..., description='The type of the progress (page or percentage)')
    value: int = Field(..., description='The value of the progress')
    progress_date: date = Field(default_factory=date.today, description='The date that progress was taken')
    rate: int | None = Field(None, description='The rate of the reading so far')
    comment: str | None = Field(None, description='The comments for the reading so far')

    @model_validator(mode='after')
    def check_value_range(self) -> 'CreateProgressRequestV2':
        if self.progress_type == 'percentage' and not (0 < self.value <= 100):
            raise ValueError('percentage must be between 1 and 100')

        if self.progress_type == 'page' and self.value < 0:
            raise ValueError('page must be a positive integer')

        return self


class GetProgressRequest(BaseModel):
    reading_id: uuid.UUID = Field(Query(..., alias='readingId', description="The id of the reading"))
    item_id: uuid.UUID | None = Field(Query(None, alias='itemId', description="The id of the item"))


class GetReadingStatsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    item_id: int = Field(..., description="The id of the item")
