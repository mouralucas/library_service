import uuid
from datetime import date

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from schemas.core import StatusSchema
from schemas.item import ItemSchema


class ProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        ...,
        serialization_alias="readingProgressId",
        description="The identification of the progress entry",
    )
    reading_id: uuid.UUID = Field(
        ..., serialization_alias="readingId", description="The id of the reading"
    )
    progress_date: date = Field(
        ...,
        serialization_alias="date",
        description="The date that the entry was created",
    )
    page: int = Field(..., serialization_alias="page", description="The current page")
    percentage: float = Field(
        ..., serialization_alias="percentage", description="The current percentage"
    )
    rate: int | None = Field(
        None, serialization_alias="rate", description="The rate for this entry"
    )
    comment: str | None = Field(
        None, serialization_alias="comment", description="The comment for this entry"
    )


class ReadingSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: uuid.UUID = Field(..., description="The id of the reading")
    item_id: int = Field(..., description="The id of the item")
    item_title: str | None = Field(None, description="The title of the item")
    start_date: date = Field(..., description="The date the reading start")
    finish_date: date | None = Field(None, description="The date the reading ends")
    number: int = Field(
        ...,
        description="The number of the reading, if it is first, second time, etc",
    )
    active: bool = Field(
        ...,
        description="If false reading could be finished or dropped, \
            if true is reading now, check status",
    )
    status_id: str = Field(..., description="The id of the status")
    status_name: str | None = Field(None, description="The name of the status")
    progress: list[ProgressSchema] | None = Field(
        None,
        description="The current progress of the reading",
    )

class ReadingStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    readings_count: int = Field(
        ...,
        serialization_alias="readingsCount",
        description="The total number of readings",
    )
    last_reading_date: date | None = Field(
        None,
        serialization_alias="lastReadingDate",
        description="The date of the last reading",
    )
    is_currently_reading: bool = Field(
        ...,
        serialization_alias="isCurrentlyReading",
        description="If there is an active reading",
    )
    current_reading_id: uuid.UUID | None = Field(
        None,
        serialization_alias="currentReadingId",
        description="The id of the current reading",
    )
    current_page: int | None = Field(
        None,
        serialization_alias="currentPage",
        description="The current page of the reading",
    )
    current_percentage: float | None = Field(
        None,
        serialization_alias="currentPercentage",
        description="The current percentage of the reading",
    )
    last_readings: list[ReadingSchema] | None = Field(
        None, serialization_alias="lastReadings", description="The last readings"
    )

    @model_validator(mode="after")
    def validate_response(self):
        if self.is_currently_reading and self.current_reading_id is None:
            raise ValueError(
                "If there is an active reading, currentReadingId must be provided"
            )

        return self
