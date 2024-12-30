from pydantic import BaseModel, Field


class CreateAuthorRequest(BaseModel):
    name: str = Field(..., alias='authorName', description='The name of the author')
    country_id: str = Field(None, alias='countryId', description='The country of the author')
    language_id: str = Field(None, alias='languageId', description='The language of writing')
    description: str = Field(None, alias='description', description='The description of the author')
    is_translator: bool = Field(False, alias='isTranslator', description='Whether the author should be translated')