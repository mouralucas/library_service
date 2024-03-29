from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.reading import ReadingSchema, ProgressSchema


class CreateReadingResponse(SuccessResponseBase):
    reading: ReadingSchema = Field(..., description="The reading information")


class GetReadingResponse(SuccessResponseBase):
    quantity: int = Field(..., description="The number of returned readings")
    readings: list[ReadingSchema]


class CreateProgressionResponse(SuccessResponseBase):
    progress: ProgressSchema = Field(..., description="The reading progress information")


class CreateProgressResponse(SuccessResponseBase):
    currentReadingProgress: ProgressSchema = Field(..., description="The current reading progress for an item")


class GetProgressResponse(SuccessResponseBase):
    quantity: int = Field(..., description="The number of entries returned")
    readingProgress: list[ProgressSchema] = Field(..., description="The reading progress information")
