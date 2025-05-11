from pydantic import Field, BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel

from rolf_common.schemas import SuccessResponseBase

from schemas.item import ItemSchema
from schemas.reading import ReadingSchema, ProgressSchema


class CreateReadingResponse(BaseModel):
    reading: ReadingSchema = Field(..., description="The reading information")


class GetReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(
        serialization_alias=to_camel
    ))

    item_title: str = Field(..., description="The title of the item")
    quantity: int = Field(..., description="The number of returned readings")
    readings: list[ReadingSchema]


class GetActiveReadingsResponse(BaseModel):
    quantity: int = Field(..., description="The number of active readings")
    readings: list[ReadingSchema]


class CreateProgressResponse(SuccessResponseBase):
    item: ItemSchema = Field(..., exclude=True)
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The title of the item")
    pages_read: str | None = Field(None, serialization_alias='pagesRead', description="Total pages read so far, if pages are available in item")
    progress: ProgressSchema = Field(..., serialization_alias='readingProgress', description="The reading progress information")

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
    item: ItemSchema | None = Field(None, exclude=True)
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The title of the item")
    pages_read: str | None = Field(None, serialization_alias='pagesRead', description="Total pages read so far, if pages are available in item")
    progress: list[ProgressSchema] = Field(..., serialization_alias='readingProgress', description="The reading progress information")

    def transform(self):
        resp_str = '{latest_page}/{total_pages} - {percentage}%'.format(latest_page=str(self.progress[0].page),
                                                                        total_pages=str(self.item.pages),
                                                                        percentage=self.progress[0].percentage) \
            if self.progress and self.progress[0].page and self.item.pages else None

        self.item_title = self.item.title if self.item else None
        self.pages_read = resp_str

        return self