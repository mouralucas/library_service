from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    title: int = Field(..., alias='itemTitle', description='The name of the item')
    description: str = Field(..., alias='description', description='The description of the item')
