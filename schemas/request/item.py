from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    title: int = Field(..., alias='itemTitle', description='The name of the item')
    description: str = Field(..., alias='description', description='The description of the item')


@dataclass
class GetItemRequest:
    itemId: int = Query(None, title='Id do item', description="Identificação única do item na base de dados")
