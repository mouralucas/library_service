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

    name: str


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., alias="authorId", description="Unique id of the author")
    name: str = Field(..., serialization_alias="authorName", description="The name of the author")
