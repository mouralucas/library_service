from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.core import LanguageSchema


class CreateLanguageResponse(SuccessResponseBase):
    language: LanguageSchema = Field(..., serialization_alias='language', description='The language created')
