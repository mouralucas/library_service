from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.item import ItemService
from backend.database import db_session
from schemas.request.item import GetItemRequest, CreateItemRequest

router = APIRouter(prefix="/item")


@router.post('')
async def create_item(item: CreateItemRequest,
                      session: AsyncSession = Depends(db_session)):
    response = await ItemService(session=session).create_item(item)

    return response


@router.get('', summary='Get all items', description='Get items based on passed filters', )
async def get_items(params: GetItemRequest = Depends(),
                    session: AsyncSession = Depends(db_session)):
    response = await ItemService(session=session).get_items(params)

    return response
