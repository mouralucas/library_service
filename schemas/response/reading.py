from pydantic import Field, BaseModel, ConfigDict, AliasGenerator, model_validator
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
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(
        serialization_alias=to_camel
    ))

    quantity: int = Field(..., description="The number of active readings")
    readings: list[ReadingSchema] = Field(None, description="The list of active readings")


class CreateProgressResponse(BaseModel):
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


class GetProgressResponse(BaseModel):
    quantity: int = Field(..., description="The number of entries returned")
    item: ItemSchema | None = Field(None, exclude=True)
    item_title: str | None = Field(None, serialization_alias='itemTitle', description="The title of the item")
    pages_read: str | None = Field(None, serialization_alias='pagesRead', description="Total pages read so far, if pages are available in item")
    progress: list[ProgressSchema] = Field(..., serialization_alias='readingProgress', description="The reading progress information")

    @model_validator(mode='after')
    def compute_derived_fields(self):
        if self.item:
            self.item_title = self.item.title
            if self.progress and self.progress[0].page and self.item.pages:
                self.pages_read = '{}/{} - {}%'.format(
                    self.progress[0].page,
                    self.item.pages,
                    self.progress[0].percentage
                )
        return self

