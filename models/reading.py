import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import SQLModel
from models.item import ItemModel


class ReadingModel(SQLModel):
    __tablename__ = "reading"
    __table_args__ = {"schema": "library"}

    owner_id: Mapped[uuid.UUID] = mapped_column('owner_id')
    item_id: Mapped[int] = mapped_column('item_id')
    item: Mapped[ItemModel] = relationship('ItemModel', foreign_keys=[item_id], primaryjoin='ReadingModel.item_id == ItemModel.id')
    start_at: Mapped[str] = mapped_column('start_at')
    end_at: Mapped[str] = mapped_column('end_at')
    number: Mapped[int] = mapped_column('number')
    is_dropped: Mapped[bool] = mapped_column('is_dropped')


class ReadingProgressModel(SQLModel):
    __tablename__ = "reading_progress"
    __table_args__ = {"schema": "library"}

    reading_id: Mapped[uuid.UUID] = mapped_column('reading_id')
    reading: Mapped[ReadingModel] = relationship('ReadingModel', foreign_keys=[reading_id], primaryjoin='ReadingProgressModel.reading_id == ReadingModel.id')
    date: Mapped[str] = mapped_column('date')
    page: Mapped[int] = mapped_column('page')
    percentage: Mapped[float] = mapped_column('percentage')
    rate: Mapped[int] = mapped_column('rate')
    comment: Mapped[str] = mapped_column('comment')
