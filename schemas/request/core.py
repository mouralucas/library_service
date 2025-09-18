from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CreateLanguageRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    id: str = Field(
        ...,
        alias="languageId",
        description="Id of the language - two letter code",
        max_length=2,
    )
    name: str = Field(..., alias="languageName", description="Name of the language")
    code: str = Field(..., description="Code of the language - usually same as id")


class CreateCountryRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    id: str = Field(
        ..., alias="countryId", description="Id of the country", max_length=2
    )
    name: str = Field(..., alias="countryName", description="Name of the country")
    continent: str = Field(..., description="Continent of the country", max_length=2)
    description: str | None = Field(None, description="Description of the country")


class CreateSerieRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    name: str = Field(..., alias="serieName", description="Name of the serie")
    original_name: str | None = Field(None, description="Original name of the serie")
    description: str | None = Field(None, description="Description of the serie")
    country_id: str | None = Field(None, description="Id of the country")


class CreateCollectionRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    name: str = Field(..., alias="collectionName", description="Name of the collection")
    description: str | None = Field(None, description="Description of the collection")


class CreatePublisherRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    name: str = Field(..., alias="publisherName", description="Name of the publisher")
    description: str | None = Field(None, description="Description of the publisher")
    country_id: str | None = Field(None, description="Id of the country")
    parent_id: str | None = Field(None, description="Id of the parent publisher")


class GetStatusRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=AliasGenerator(alias=to_camel)
    )

    status_type: str = Field(..., description="Type of the status")
