from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from rolf_common.schemas import SuccessResponseBase

from schemas.core import CollectionSchema, CountrySchema, LanguageSchema, PublisherSchema, SerieSchema, StatusSchema


class CreateLanguageResponse(SuccessResponseBase):
    language: LanguageSchema = Field(..., serialization_alias='language', description='The language created')


class GetLanguageResponse(SuccessResponseBase):
    quantity: int = Field(..., description='The quantity of languages available')
    languages: list[LanguageSchema] = Field(..., serialization_alias='languages', description='The languages available')


class CreateCountryResponse(SuccessResponseBase):
    country: CountrySchema = Field(..., serialization_alias='country', description='The country created')


class GetCountryResponse(SuccessResponseBase):
    quantity: int = Field(..., description='The quantity of countries available')
    countries: list[CountrySchema] = Field(..., serialization_alias='countries', description='The countries available')


class CreateSerieResponse(SuccessResponseBase):
    serie: SerieSchema = Field(..., serialization_alias='serie', description='The serie created')


class GetSeriesResponse(SuccessResponseBase):
    quantity: int = Field(..., description='The quantity of series available')
    series: list[SerieSchema] = Field(..., serialization_alias='series', description='The series available')


class CreateCollectionResponse(SuccessResponseBase):
    collection: CollectionSchema = Field(..., serialization_alias='collection', description='The collection created')


class GetCollectionResponse(SuccessResponseBase):
    quantity: int = Field(..., description='The quantity of collections available')
    collections: list[CollectionSchema] = Field(..., serialization_alias='collections', description='The collections available')


class CreatePublisherResponse(SuccessResponseBase):
    publisher: PublisherSchema = Field(..., description='The publisher created')


class GetPublisherResponse(SuccessResponseBase):
    quantity: int = Field(..., description='The quantity of publishers available')
    publishers: list[PublisherSchema] = Field(..., description='The publishers available')


class GetStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=AliasGenerator(serialization_alias=to_camel))

    quantity: int = Field(..., description='The quantity of statuses available')
    statuses: list[StatusSchema] = Field(..., description='The list of available statuses')
