from pydantic import BaseModel, Field
from sqlalchemy import DateTime


class CreateReading(BaseModel):
    item_id: int = Field(..., alias='itemId', description="The id of the item")
    start_at: str = Field(..., alias='startAt', description="The date that the user start reading the item")
    finish_at: str = Field(None, alias='finishAt', description="The date that the user finish reading the item")
    is_dropped: bool = Field(False, alias='isDropped', description="Indicate if the user has dropped the item")

