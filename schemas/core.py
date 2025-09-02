from datetime import date

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class LanguageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ..., serialization_alias="languageId", description="Unique language identifier"
    )
    name: str = Field(
        ..., serialization_alias="languageName", description="Name of language"
    )
    code: str | None = Field(
        None, serialization_alias="languageCode", description="Code of language"
    )


class StatusSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: str = Field(
        ..., serialization_alias="statusId", description="The id of the status"
    )
    name: str = Field(..., description="The name of the status")
    description: str | None = Field(None, description="The description of the status")
    order: int | None = Field(None, description="The order of the status")
    type: str = Field(
        ..., serialization_alias="itemType", description="The type of the status"
    )


class CountrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., serialization_alias="countryId")
    name: str = Field(..., serialization_alias="countryName")
    continent: str
    description: str | None


class SerieSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: int = Field(
        ..., serialization_alias="serieId", description="Unique identifier of the serie"
    )
    name: str = Field(
        ..., serialization_alias="serieName", description="The name of the serie"
    )
    original_name: str | None = Field(
        None, description="The original name of the serie"
    )
    description: str | None = Field(None, description="The description of the serie")
    country_id: str | None = Field(None, description="The id of the country")
    country_name: str | None = Field(None, description="The name of the country")


class CollectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        serialization_alias="collectionId",
        description="Unique identifier of the collection",
    )
    name: str = Field(
        ...,
        serialization_alias="collectionName",
        description="The name of the collection",
    )
    description: str | None = Field(
        None,
        description="The description of the collection",
    )


class PublisherSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: int = Field(
        ...,
        serialization_alias="publisherId",
        description="Unique identifier of the publisher",
    )
    name: str = Field(
        ...,
        serialization_alias="publisherName",
        description="The name of the publisher",
    )
    description: str | None = Field(
        None, description="The description of the publisher"
    )
    country_id: str | None = Field(None, description="The id of the country")
    country_name: str | None = Field(
        None, description="The name of the publisher country"
    )
    country: CountrySchema | None = Field(None, description="The country")
    parent_id: int | None = Field(None, description="The parent of the publisher")


class AuthorSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
    )

    id: int = Field(
        ..., serialization_alias="authorId", description="Unique id of the author"
    )
    name: str = Field(
        ..., serialization_alias="authorName", description="The name of the author"
    )
    birth_date: date | None = Field(None, description="The birth date of the author")
    description: str | None = Field(None, description="The description of the author")
    country_id: str | None = Field(None, description="The country id of the author")
    country_name: str | None = Field(None, description="The country name of the author")
    country: CountrySchema | None = Field(None, description="The country of the author")
    language_id: str | None = Field(None, description="The language id of the author")
    language_name: str | None = Field(
        None, description="The language name of the author"
    )
    language: LanguageSchema | None = Field(
        None, description="The language of the author"
    )
