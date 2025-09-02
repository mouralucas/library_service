from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from rolf_common.schemas.base import DefaultModel

from schemas.item import ItemSchema


class CreateItemResponse(DefaultModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    item: ItemSchema = Field(..., description="The item created")


class GetItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    quantity: int = Field(..., description="Quantity of items")
    items: list[ItemSchema] | None = Field(..., description="List of the items")
