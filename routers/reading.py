from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from backend.session import get_db_session
from schemas.reading import CreateReadingRequest, GetReadingRequest
from services.reading import ReadingService

router = APIRouter(prefix="/reading")


@router.post('', summary='Create a reading', description='Create a new reading for selected item', )
def create_reading(params: CreateReadingRequest, session: AsyncSession = Depends(get_db_session)):
    response = ReadingService(session=session).create_reading(reading=params)

    return response


@router.get('', summary='Get a reading', description='Get a reading by id')
async def get_reading(param: GetReadingRequest = Depends(), session: AsyncSession = Depends(get_db_session)):
    response = await ReadingService(session=session).get_reading()

    return response


