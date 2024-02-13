from pydantic import BaseModel, ConfigDict, Field


class SuccessResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool = Field(None, serialization_alias='success')
    status_code: int = Field(..., serialization_alias='statusCode')
