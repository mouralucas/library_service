from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.core import LanguageSchema, CountrySchema, SerieSchema, CollectionSchema


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
