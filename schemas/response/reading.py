from pydantic import Field

from rolf_common.schemas import SuccessResponseBase

from schemas.item import ItemSchema
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
    item: ItemSchema = Field(..., description="The item information", exclude=True)
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The title of the item")
    pages_read: str | None = Field(None, serialization_alias='pages_read', description="The title of the item")
    progress: ProgressSchema = Field(..., description="The reading progress information")

    def transform(self):
        resp_str = '{latest_page}/{total_pages} - {percentage}%'.format(latest_page=str(self.progress.page),
                                                                       total_pages=str(self.item.pages),
                                                                       percentage=self.progress.percentage) if self.progress.page and self.item.pages else None

        self.item_title = self.item.title
        self.pages_read = resp_str

        return self


# class CreateProgressResponse(SuccessResponseBase):
#     currentReadingProgress: ProgressSchema = Field(..., description="The current reading progress for an item")


class GetProgressResponse(SuccessResponseBase):
    quantity: int = Field(..., description="The number of entries returned")
    readingProgress: list[ProgressSchema] = Field(..., description="The reading progress information")
