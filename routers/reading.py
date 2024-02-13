from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.session import get_db_session
from schemas.reading import CreateReadingRequest, GetReadingRequest, GetReadingResponse
from services.reading import ReadingService

router = APIRouter(prefix="/reading")


@router.post('', summary='Create a reading', description='Create a new reading for selected item', )
def create_reading(params: CreateReadingRequest, session: AsyncSession = Depends(get_db_session)):
    response = ReadingService(session=session).create_reading(reading=params)

    return response


@router.get('', summary='Get a reading', description='Get a reading by id')
async def get_reading(params: GetReadingRequest = Depends(),
                      session: AsyncSession = Depends(get_db_session)
                      ) -> list[GetReadingResponse]:
    response = await ReadingService(session=session).get_reading(params=params)

    return response
