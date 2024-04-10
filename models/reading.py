from __future__ import annotations

import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import SQLModel
from models.core import StatusModel
from models.item import ItemModel


class ReadingModel(SQLModel):
    __tablename__ = "reading"
    __table_args__ = {"schema": "library"}

    owner_id: Mapped[uuid.UUID]
    active: Mapped[bool] = mapped_column('active', default=True)
    item_id: Mapped[int] = mapped_column('item_id')
    item: Mapped[ItemModel] = relationship('ItemModel', foreign_keys=[item_id], lazy='joined', primaryjoin='ReadingModel.item_id == ItemModel.id')
    start_date: Mapped[datetime.date]
    finish_date: Mapped[datetime.date]
    number: Mapped[int] = mapped_column('number', default=1)
    status_id: Mapped[str] = mapped_column(ForeignKey('public.status.id'))
    status: Mapped['StatusModel'] = relationship(foreign_keys=[status_id])
    progress: Mapped[list['ReadingProgressModel']] = relationship(back_populates='reading', lazy='noload')


class ReadingProgressModel(SQLModel):
    __tablename__ = "reading_progress"
    __table_args__ = {"schema": "library"}

    reading_id: Mapped[uuid.UUID] = mapped_column("reading_id", ForeignKey("library.reading.id"))
    reading: Mapped["ReadingModel"] = relationship(back_populates='progress')
    date: Mapped[datetime.date] = mapped_column('date')
    page: Mapped[int] = mapped_column('page')
    percentage: Mapped[float] = mapped_column('percentage')
    rate: Mapped[int] = mapped_column('rate')
    comment: Mapped[str] = mapped_column('comment')
