import datetime
import uuid

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from schemas.request.base import OrderBySchemaRequest


class CreateItemRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    id: int | None = Field(None, description="Id of the item")
    owner_id: uuid.UUID | None = Field(None, description="Id of the owner")
    last_status_id: str | None = Field(
        None, description="Id of the last status of the item"
    )
    last_status_date: datetime.date | None = Field(
        ..., description="Date of the last status of the item"
    )
    main_author_id: int | None = Field(
        None, description="The id of the main author of the item"
    )
    authors_ids: list[int] | None = Field(
        None, description="The ids of other authors of the item"
    )
    title: str = Field(..., description="The name of the item")
    subtitle: str | None = Field(None, description="The subtitle of the item")
    # title_original: str | None = Field(
    #     None, description="The original title of the item"
    # )
    # subtitle_original: str | None = Field(
    #     None, description="The original subtitle of the item"
    # )
    isbn: str | None = Field(None, description="The ISBN of the item")
    type: str | None = Field(
        None, alias="itemTypeId", description="The type of the item"
    )
    pages: int | None = Field(0, description="The number of pages of the item")
    volume: int | None = Field(0, description="The volume of the item")
    publication_date: datetime.date | None = Field(
        None, description="The date of the publish"
    )
    original_publication_date: datetime.date | None = Field(
        None, description="The date of the publish"
    )
    serie_id: int = Field(0, description="The id of the serie")
    collection_id: int = Field(0, description="The id of the collection")
    publisher_id: int | None = Field(None, description="The publisher of the item")
    format: str | None = Field(
        None, alias="formatId", description="The id of the format"
    )
    language_id: str | None = Field(None, description="The id of the language")
    cover_price: float | None = Field(None, description="The price of the item")
    paid_price: float | None = Field(None, description="The price of the item")
    summary: str | None = Field(None, description="The summary of the item")
    observation: str | None = Field(None, description="The observation of the item")
    location_id: int = Field(..., description="The id of the location")

    cover: str = Field(
        "library/item/cover/no_cover.png", description="Cover of the item"
    )


class UpdateItemRequest(CreateItemRequest):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    # Is basically the same as "Create Item", but without default and required = true
    # and id is required
    id: int = Field(..., description="Id of the item")
    title: str | None = Field(None, description="The name of the item")
    last_status_date: datetime.date | None = Field(
        None, description="Date of the last status of the item"
    )
    pages: int | None = Field(None, description="The number of pages of the item")
    volume: int | None = Field(None, description="The volume of the item")
    edition: int | None = Field(None, description="The edition of the item")
    serie_id: int | None = Field(None, description="The id of the serie")
    collection_id: int | None = Field(None, description="The id of the collection")
    cover: str | None = Field(None, description="Cover of the item")
    location_id: int | None = Field(None, description="The id of the location")


class GetItemSummaryRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    id: int | None = Field(None, ge=1, alias="id")
    title: str | None = Field(None, min_length=3)
    main_author_id: int | None = Field(None)
    itemTypeId: str | None = Field(None)
    status_id: str | None = Field(None)
    active_goal: bool= Field(False, description="If true, return only items with active reading goal for the current year")
    active_reading: bool = Field(False, description="If true, return only items with active reading")
    order_by: list[OrderBySchemaRequest] | None = Field(None)
    
class GetItemRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    id: int | None = Field(None, ge=1, alias="itemId")
    title: str | None = Field(None, min_length=3, alias="title")
    main_author_id: int | None = Field(None, alias="mainAuthorId")
    type: str | None = Field(None, alias="itemTypeId")
    status_id: str | None = Field(None, alias="statusId")
    order_by: list[OrderBySchemaRequest] | None = Field(None)


class GetItemsByLocationRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    location_ids: list[int] | None = Field(
        None, description="The list of location ids to filter the items"
    )
