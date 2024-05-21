from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.core import LanguageSchema, CountrySchema


class CreateLanguageResponse(SuccessResponseBase):
    language: LanguageSchema = Field(..., serialization_alias='language', description='The language created')


class GetLanguageResponse(SuccessResponseBase):
    languages: list[LanguageSchema] = Field(..., serialization_alias='languages', description='The languages available')


class CreateCountryResponse(SuccessResponseBase):
    country: CountrySchema = Field(..., serialization_alias='country', description='The country created')


class GetCountryResponse(SuccessResponseBase):
    countries: list[CountrySchema] = Field(..., serialization_alias='countries', description='The countries available')