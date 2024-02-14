from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.session import get_db_session
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, CreateProgressResponse, GetProgressResponse
from services.reading import ReadingService

router = APIRouter(prefix="/reading")


@router.post('', summary='Create a reading', description='Create a new reading for selected item', )
def create_reading(params: CreateReadingRequest, session: AsyncSession = Depends(get_db_session)):
    response = ReadingService(session=session).create_reading(reading=params)

    return response


@router.get('', summary='Get readings', description='Get all readings for a item')
async def get_reading(params: GetReadingRequest = Depends(),
                      session: AsyncSession = Depends(get_db_session)
                      ) -> GetReadingResponse:
    response = await ReadingService(session=session).get_reading(params=params)

    return response


@router.post('/progress', summary='Add progress', description='Add a new progress for a reading')
async def create_reading_progress(progress: CreateProgressRequest, session: AsyncSession = Depends(get_db_session)) -> CreateProgressResponse:
    response = await ReadingService(session=session).create_progress(progress=progress)

    return response


@router.get('/progress', summary='Get progress', description='Get the progress for a reading', response_model_exclude_none=True)
async def get_reading_progress(params: GetProgressRequest = Depends(), session: AsyncSession = Depends(get_db_session)) -> GetProgressResponse:
    response = await ReadingService(session=session).get_progress(params=params)

    return response
