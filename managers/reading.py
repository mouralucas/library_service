from typing import Type

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from managers.base import BaseDataManager
from models.base import SQLModel
from models.reading import ReadingModel, ReadingProgressModel
from schemas.reading import ProgressSchema, ReadingSchema
from schemas.request.reading import CreateReadingRequest


class ReadingDataManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_reading(self, reading: ReadingModel):
        new_reading = self.add_one(reading)

    async def get_reading_by_id(self, reading_id, transform_result: bool = False) -> ReadingModel:
        stmt = select(ReadingModel).where(ReadingModel.id == reading_id)

        reading: BaseModel = await self.get_only_one(stmt, ReadingSchema)

        return reading.transform() if transform_result else reading

    async def get_readings(self, params: dict):
        stmt = select(ReadingModel)

        for key, value in params.items():
            stmt = stmt.where(getattr(ReadingModel, key) == value)

        readings = self.get_all(stmt, ReadingSchema)

    async def create_progress(self, progress: ReadingProgressModel) -> SQLModel:
        new_progress = await self.add_one(progress)

        return new_progress

    async def get_progress(self, reading_id):
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id)

        progress_list = self.get_all(stmt, ProgressSchema)

        return progress_list

    async def get_latest_progress(self, reading_id):
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.reading_id == reading_id).order_by(ReadingProgressModel.date.desc())

        latest_progress = await self.get_first(stmt, ProgressSchema)

        return latest_progress
