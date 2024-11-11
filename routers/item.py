import uuid

from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database import get_session
from schemas.request.item import GetItemRequest, CreateItemRequest, UpdateItemRequest
from schemas.response.item import GetItemResponse, CreateItemResponse
from services.item import ItemService

router = APIRouter(prefix="/item", tags=['Items'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('', summary='Get items', description='Get items based on passed filters', )
async def get_items(
        params: GetItemRequest = Depends(),
        session: AsyncSession = Depends(get_session),
        user: RequiredUser = Security(get_user, scopes=['permission_test', 'another_permission_test']),
) -> GetItemResponse:
    response = await ItemService(session=session, user=user).get_items(params)

    return response


@router.post('', summary='Create item', status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
async def create_item(
        item: CreateItemRequest,
        session: AsyncSession = Depends(get_session),
        user: RequiredUser = Security(get_user)
) -> CreateItemResponse:
    response = await ItemService(session=session, user=user).create_item(item)

    return response


@router.patch('', description='Update item')
async def update_item(
        item: UpdateItemRequest,
        session: AsyncSession = Depends(get_session),
        user: RequiredUser = Security(get_user)
) -> CreateItemResponse:
    response = await ItemService(session=session, user=user).update_item(item)

    return response
