import uuid

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class GetItemsV2Request(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    metadata_id: uuid.UUID | None = Field(None)
