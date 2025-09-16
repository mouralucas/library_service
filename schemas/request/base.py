from typing import Literal

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OrderBySchemaRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=AliasGenerator(alias=to_camel),
    )

    field: str = Field(..., description="The field which to order by")
    direction: Literal["ASC", "DESC"] = Field(
        "ASC", description="The direction for the order by, default: ASC"
    )
