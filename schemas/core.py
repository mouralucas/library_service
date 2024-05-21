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
