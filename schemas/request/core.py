from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CreateLanguageRequest(BaseModel):
    id: str = Field(..., alias="id", description="Id of the language - two letter code", max_length=2)
    name: str = Field(..., alias='name', description="Name of the language")
    code: str = Field(..., alias='code', description="Code of the language - usually same as id")


class CreateCountryRequest(BaseModel):
    id: str = Field(..., alias="id", description="Id of the country", max_length=2)
    name: str = Field(..., alias='name', description="Name of the country")
    continent: str = Field(..., alias='continent', description="Continent of the country", max_length=2)
    description: str = Field(None, alias='description', description="Description of the country")


class CreateSerieRequest(BaseModel):
    name: str = Field(..., alias='serieName', description="Name of the serie")
    original_name: str = Field(None, alias='originalSerieName', description="Original name of the serie")
    description: str = Field(None, alias='serieDescription', description="Description of the serie")
    country_id: str = Field(None, alias='countryId', description="Id of the country")


class CreateCollectionRequest(BaseModel):
    name: str = Field(..., alias='collectionName', description="Name of the collection")
    description: str = Field(None, alias='description', description="Description of the collection")


class CreatePublisherRequest(BaseModel):
    name: str = Field(..., alias='publisherName', description="Name of the publisher")
    description: str = Field(None, alias='description', description="Description of the publisher")
    country_id: str = Field(None, alias='countryId', description="Id of the country")
    parent_id: str = Field(None, alias='parentId', description="Id of the parent publisher")


class GetStatusRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(
                                  alias=to_camel
                              ))
    item_type: str = Field(..., description="Type of the item")