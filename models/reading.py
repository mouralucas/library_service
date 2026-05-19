from __future__ import annotations

import datetime
import uuid

from rolf_common.models import SQLModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.core import StatusModel
from models.item import ItemModel


class ReadingModel(SQLModel):
    __tablename__ = "reading"

    owner_id: Mapped[uuid.UUID] = mapped_column("owner_id")
    active: Mapped[bool] = mapped_column("active", default=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped[ItemModel] = relationship(foreign_keys=[item_id], lazy="subquery")
    start_date: Mapped[datetime.date]
    finish_date: Mapped[datetime.date] = mapped_column("finish_date", nullable=True)
    number: Mapped[int] = mapped_column("number", default=1)
    status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    status: Mapped[StatusModel] = relationship(
        foreign_keys=[status_id], lazy="subquery"
    )
    progress: Mapped[list[ReadingProgressModel]] = relationship(
        back_populates="reading", lazy="noload"
    )


class ReadingProgressModel(SQLModel):
    __tablename__ = "reading_progress"

    reading_id: Mapped[uuid.UUID] = mapped_column(
        "reading_id", ForeignKey("reading.id")
    )
    reading: Mapped[ReadingModel] = relationship(back_populates="progress")
    item_id: Mapped[int] = mapped_column("item_id", ForeignKey("item.id"))
    item: Mapped[ItemModel] = relationship(foreign_keys=[item_id], lazy="subquery")
    progress_date: Mapped[datetime.date] = mapped_column("progress_date")
    page: Mapped[int] = mapped_column("page", nullable=True)
    percentage: Mapped[float] = mapped_column("percentage", nullable=True)
    rate: Mapped[int | None] = mapped_column("rate", nullable=True)
    comment: Mapped[str | None] = mapped_column("comment", nullable=True)


class ReadingQueueModel(SQLModel):
    __tablename__ = "reading_queue"

    owner_id: Mapped[uuid.UUID] = mapped_column("owner_id")
    item_id: Mapped[int] = mapped_column("item_id", ForeignKey("item.id"))
    item: Mapped[ItemModel] = relationship(foreign_keys=[item_id], lazy="subquery")
    achieved: Mapped[bool] = mapped_column(default=False)
    date_achieved: Mapped[datetime.datetime] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column("year", doc="Year of the goal")
