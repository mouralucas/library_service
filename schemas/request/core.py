from pydantic import BaseModel, Field


class CreateLanguageRequest(BaseModel):
    id: str = Field(..., alias="id", description="Id of the language - two letter code", max_length=2)
    name: str = Field(..., alias='name', description="Name of the language")
    code: str = Field(..., alias='code', description="Code of the language - usually same as id")

