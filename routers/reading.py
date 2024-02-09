from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.reading import CreateReading
from services.reading import ReadingService

router = APIRouter(prefix="/reading")


@router.post('/', summary='Create a reading', description='Create a new reading for selected item', )
def create_reading(params: CreateReading, session: Session = Depends(create_session)):
    response = ReadingService(session=session).create_reading(reading=params)

    return response
