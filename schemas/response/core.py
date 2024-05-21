from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.core import LanguageSchema


class CreateLanguageResponse(SuccessResponseBase):
    language: LanguageSchema = Field(..., serialization_alias='language', description='The language created')


class GetLanguageResponse(SuccessResponseBase):
    languages: list[LanguageSchema] = Field(..., serialization_alias='languages', description='The languages available')
