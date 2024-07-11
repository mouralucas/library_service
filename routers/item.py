import uuid
from typing import Any

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from httpx import Request, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas.response.item import GetItemResponse, CreateItemResponse
from services.item import ItemService
from backend.database import db_session
from schemas.request.item import GetItemRequest, CreateItemRequest, UpdateItemRequest

from rolf_common.services import get_user

router = APIRouter(prefix="/item")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('', summary='Get items', description='Get items based on passed filters', )
async def get_items(params: GetItemRequest = Depends(),
                    session: AsyncSession = Depends(db_session)) -> GetItemResponse:
    response = await ItemService(session=session).get_items(params)

    return response


@router.post('', status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
async def create_item(item: CreateItemRequest,
                      session: AsyncSession = Depends(db_session)) -> CreateItemResponse:
    # user_id: uuid.UUID = Security(get_user)):
    response = await ItemService(session=session).create_item(item)

    return response


@router.patch('', description='Update item')
async def update_item(item: UpdateItemRequest,
                      session: AsyncSession = Depends(db_session)) -> CreateItemResponse:
    response = await ItemService(session=session).update_item(item)

    return response
