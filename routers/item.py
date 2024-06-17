from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.item import ItemService
from backend.database import db_session
from schemas.request.item import GetItemRequest, CreateItemRequest

from rolf_common.services import require_user

router = APIRouter(prefix="/item")


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_item(item: CreateItemRequest,
                      session: AsyncSession = Depends(db_session),
                      user: None = Depends(require_user)):
    response = await ItemService(session=session).create_item(item)

    return response


@router.get('', summary='Get all items', description='Get items based on passed filters', )
async def get_items(params: GetItemRequest = Depends(),
                    session: AsyncSession = Depends(db_session)):
    response = await ItemService(session=session).get_items(params)

    return response
