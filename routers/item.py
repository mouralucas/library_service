from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.session import create_session
from schemas.item import Request

router = APIRouter(prefix="/item")


@router.get('/', summary='Get all items', description='Get items based on passed filters', )
def get_items(params: Request = Depends(), db: Session = Depends(create_session)):
    return {"itemId": params.list_parameter}
