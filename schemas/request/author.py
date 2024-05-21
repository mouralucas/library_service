from pydantic import BaseModel, Field


class CreateAuthorRequest(BaseModel):
    name: str = Field(..., alias='authorName', description='The name of the author')
    country_id: str = Field(None, alias='countryId', description='The country of the author')
    language_id: str = Field(None, alias='countryId', description='The language of writing')
