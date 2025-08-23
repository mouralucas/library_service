from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class GetAuthorsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    author_id: int | None = Field(None)


class CreateAuthorRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(
        alias=to_camel
    ))

    name: str = Field(..., alias='authorName', description='The name of the author')
    country_id: str = Field(None, description='The country of the author')
    language_id: str = Field(None, description='The language of writing')
    description: str = Field(None, description='The description of the author')
    is_translator: bool = Field(False, description='Whether the author should be translated')
