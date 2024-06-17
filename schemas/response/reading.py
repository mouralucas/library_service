from pydantic import Field

from rolf_common.schemas import SuccessResponseBase
from schemas.reading import ReadingSchema, ProgressSchema


class CreateReadingResponse(SuccessResponseBase):
    reading: ReadingSchema = Field(..., description="The reading information")


class GetReadingResponse(SuccessResponseBase):
    item_title: str = Field(..., description="The title of the item")
    quantity: int = Field(..., description="The number of returned readings")
    readings: list[ReadingSchema]


class GetActiveReadingsResponse(SuccessResponseBase):
    quantity: int = Field(..., description="The number of active readings")
    readings: list[ReadingSchema]


class CreateProgressResponse(SuccessResponseBase):
    progress: ProgressSchema = Field(..., description="The reading progress information")


# class CreateProgressResponse(SuccessResponseBase):
#     currentReadingProgress: ProgressSchema = Field(..., description="The current reading progress for an item")


class GetProgressResponse(SuccessResponseBase):
    quantity: int = Field(..., description="The number of entries returned")
    readingProgress: list[ProgressSchema] = Field(..., description="The reading progress information")
