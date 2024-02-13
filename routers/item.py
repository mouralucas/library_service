from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.session import get_db_session
from schemas.item import Request

router = APIRouter(prefix="/item")


@router.get('/', summary='Get all items', description='Get items based on passed filters', )
def get_items(params: Request = Depends(), session: AsyncSession = Depends(get_db_session)):
    return {"itemId": params.list_parameter}
