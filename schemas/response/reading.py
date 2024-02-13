import uuid

from pydantic import Field

from schemas.base import SuccessResponseBase
from schemas.reading import ReadingSchema


class GetReadingResponse(SuccessResponseBase):
    reading: list[ReadingSchema]

