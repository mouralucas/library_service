import datetime

from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from managers.item import ItemManager
from managers.reading import ReadingDataManager
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ReadingSchema
from schemas.request.reading import CreateReadingRequest, GetReadingRequest, CreateProgressRequest, GetProgressRequest
from schemas.response.reading import GetReadingResponse, GetProgressResponse, CreateProgressResponse, CreateReadingResponse, GetActiveReadingsResponse
from services.base import BaseService


class ReadingService(BaseService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.item_pages = None

    async def create_reading(self, reading: CreateReadingRequest) -> CreateReadingResponse:
        """ TODO:
                1: Check if the item already have a reading
        """
        param = {
            'item_id': reading.item_id
        }
        previous_readings = await ReadingDataManager(self.session).get_readings(params=param)
        last_reading = previous_readings[0] if previous_readings else None

        # Cannot start a new reading with another still active
        if last_reading and last_reading.active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe uma leitura ativa para este item')

        # The new reading cannot start before the last one finishes
        if last_reading and last_reading.finish_date and last_reading.finish_date > reading.start_date:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Uma leitura não pode ser iniciada antes de finalizar a anterior')

        # Change to ReadingModel(**reading)?
        new_reading = ReadingModel(
            owner_id=reading.owner_id,
            item_id=reading.item_id,
            number=len(previous_readings) + 1 if previous_readings else 1,
            start_date=reading.start_date,
            finish_date=reading.finish_date,
            status_id='reading'  # maybe a param? If a param, update status column in Item model?
        )

        new_reading = await ReadingDataManager(self.session).create_reading(reading=new_reading)
        response = CreateReadingResponse(
            status_code=status.HTTP_201_CREATED,
            reading=ReadingSchema.model_validate(new_reading).transform()
        )
        return response

    async def get_reading(self, params: GetReadingRequest) -> GetReadingResponse:
        stmt = select(ReadingModel).where(ReadingModel.item_id == params.item_id)
        if params.get_progress:
            stmt = stmt.options(joinedload(ReadingModel.progress))

        item = await ItemManager(self.session).get_item_by_id(item_id=params.item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Item não encontrado')

        readings = await ReadingDataManager(self.session).get_all(stmt, unique_result=True)

        response = GetReadingResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            item_title=item.title,
            quantity=len(readings) if readings else 0,
            readings=[ReadingSchema.model_validate(reading) for reading in readings] if readings else []
        )

        return response

    async def get_active_readings(self) -> GetActiveReadingsResponse:
        stmt = select(ReadingModel).where(ReadingModel.active == True)

        readings = await ReadingDataManager(self.session).get_all(stmt)

        response = GetActiveReadingsResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(readings) if readings else 0,
            readings=[ReadingSchema.model_validate(reading).transform() for reading in readings] if readings else []
        )

        return response

    async def create_progress(self, progress: CreateProgressRequest) -> CreateProgressResponse:
        # TODO: Rules:
        #   One entry must not save a page and/or percentage less than the last entry
        reading = await ReadingDataManager(self.session).get_reading_by_id(progress.reading_id)
        if not reading:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Leitura não encontrada')
        last_progress = await ReadingDataManager(self.session).get_latest_progress(progress.reading_id)

        self.item_pages = reading.item.pages

        # if (last_progress and item_pages) and (last_progress.page > progress.page or last_progress.percentage > progress.percentage):
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Um registo não pode ter paginas/percentagem menor que o registro anterior')

        # Only one entry per day is allowed
        if last_progress and last_progress.date == datetime.datetime.now().date():
            progress_updated = await ReadingDataManager(session=self.session).update_progress(self.__set_values(last_progress, progress.page, progress.percentage), {'page': progress.page})
            new_entry = progress_updated
        else:
            new_progress_entry = ReadingProgressModel(
                reading_id=reading.id,
                date=datetime.datetime.now().date(),
                rate=progress.rate,
                comment=progress.comment
            )

            new_entry = await ReadingDataManager(self.session).create_progress(progress=self.__set_values(new_progress_entry, progress.page, progress.percentage))

        response = CreateProgressResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            currentReadingProgress=new_entry
        )

        return response

    async def get_progress(self, params: GetProgressRequest) -> GetProgressResponse:
        progress = await ReadingDataManager(self.session).get_progress(reading_id=params.reading_id)

        response = GetProgressResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            quantity=len(progress) if progress else 0,
            readingProgress=progress if progress else []
        )

        return response

    def __set_values(self, progress_entry: ReadingProgressModel, page, percentage):
        if page is not None:
            perc = ((page / self.item_pages) * 100) if self.item_pages else 0

            progress_entry.page = page
            progress_entry.percentage = perc

        if percentage is not None:
            page = (percentage / 100) * self.item_pages if self.item_pages else 0
            progress_entry.page = int(page)
            progress_entry.percentage = percentage

        return progress_entry
