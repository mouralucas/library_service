from dataclasses import dataclass
import uuid
from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class GetItemRequest:
    itemId: int = Query(..., title='Id do item', description="Identificação única do item na base de dados")


@dataclass
class Request:
    scalar_parameter: int = Query(None)
    list_parameter: list[int] = Query(None)


class GetItemResponse(BaseModel):
    itemId: int = Field(..., title='Id do item', description="")
    itemName: str = Field(..., title='Nome do item')
