from pydantic import BaseModel, Field, ConfigDict


class LanguageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
