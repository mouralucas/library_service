from pydantic import BaseModel, Field, ConfigDict


class LanguageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    code: str


class StatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CountrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    continent: str
    description: str | None


class SerieSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias="serieId", description="Unique identifier of the serie")
    name: str = Field(..., serialization_alias="serieName", description="The name of the serie")


class CollectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias="collectionId", description="Unique identifier of the collection")
    name: str = Field(..., serialization_alias="collectionName", description="The name of the collection")
    description: str | None = Field(None, serialization_alias="description", description="The description of the collection")


class PublisherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., serialization_alias="publisherName", description="The name of the publisher")
    description: str | None = Field(None, serialization_alias="description", description="The description of the publisher")
    country: CountrySchema | None = Field(None, serialization_alias="country", description="The country")
    parent_id: str | None = Field(None, serialization_alias="parentId", description="The parent of the publisher")


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., serialization_alias="authorId", description="Unique id of the author")
    name: str = Field(..., serialization_alias="authorName", description="The name of the author")
    country_id: str | None = Field(None, serialization_alias="countryId", description="The country id of the author")
    country: CountrySchema | None = Field(None, serialization_alias="country", description="The country of the author")
    language_id: str | None = Field(None, serialization_alias="languageId", description="The language id of the author")
    language: LanguageSchema | None = Field(None, serialization_alias="language", description="The language of the author")
