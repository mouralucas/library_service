from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from schemas.item import ItemSchema
from schemas.reading import ProgressSchema, ReadingSchema, ReadingStats


class CreateReadingResponse(BaseModel):
    reading: ReadingSchema = Field(..., description="The reading information")


class GetReadingResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    item_title: str = Field(..., description="The title of the item")
    quantity: int = Field(..., description="The number of returned readings")
    readings: list[ReadingSchema] | None = Field(
        None, description="The list of readings"
    )


class GetActiveReadingsResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    quantity: int = Field(..., description="The number of active readings")
    readings: list[ReadingSchema] | None = Field(
        None, description="The list of active readings"
    )


class CreateProgressResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    item: ItemSchema = Field(..., exclude=True)
    item_title: str | None = Field(None, description="The title of the item")
    pages_read: str | None = Field(
        None, description="Total pages read so far, if pages are available in item"
    )
    progress: ProgressSchema = Field(
        ...,
        serialization_alias="readingProgress",
        description="The reading progress information",
    )

    @model_validator(mode="after")
    def transform(self):
        resp_str = (
            f"{str(self.progress.page)}/{str(self.item.pages)} \
                - {self.progress.percentage}%"
            if self.progress.page and self.item.pages
            else None
        )

        self.item_title = self.item.title
        self.pages_read = resp_str

        return self


class GetProgressResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    quantity: int = Field(..., description="The number of entries returned")
    item: ItemSchema | None = Field(None, exclude=True)
    item_title: str | None = Field(None, description="The title of the item")
    pages_read: str | None = Field(
        None, description="Total pages read so far, if pages are available in item"
    )
    progress: list[ProgressSchema] = Field(
        ...,
        serialization_alias="readingProgress",
        description="The reading progress information",
    )

    @model_validator(mode="after")
    def compute_derived_fields(self):
        if self.item:
            self.item_title = self.item.title
            if self.progress and self.progress[0].page and self.item.pages:
                self.pages_read = f"{self.progress[0].page}\
                    /{self.item.pages} - {self.progress[0].percentage}%"
        return self


class GetReadingStatsResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    stats: ReadingStats = Field(..., description="The reading statistics")
