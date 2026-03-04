from datetime import date

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class GetAuthorsRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    author_id: int | None = Field(None)


class CreateAuthorRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    name: str = Field(..., description="The name of the author")
    country_id: str | None = Field(None, description="The country of the author")
    language_id: str | None = Field(None, description="The language of writing")
    description: str | None = Field(None, description="The description of the author")
    birth_date: date | None = Field(None)
    is_translator: bool = Field(
        False, description="Whether the author should be translated"
    )

    @field_validator("country_id", "language_id", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value
