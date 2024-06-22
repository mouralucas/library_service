import uuid
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.core import (LanguageModel, StatusModel, CountryModel, AuthorModel,
                         SerieModel, CollectionModel, PublisherModel)
from rolf_common.models import SQLModel


# TODO: remove all selectin after tests
class ItemModel(SQLModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column('id', primary_key=True)
    owner_id: Mapped[uuid.UUID]
    isbn: Mapped[str] = mapped_column('isbn', nullable=True)
    isbn10: Mapped[str] = mapped_column('isbn10', nullable=True)

    title: Mapped[str]
    title_original: Mapped[str] = mapped_column('title_original', nullable=True)
    subtitle: Mapped[str] = mapped_column('subtitle', nullable=True)
    subtitle_original: Mapped[str] = mapped_column('subtitle_original', nullable=True)
    pages: Mapped[int] = mapped_column('pages', default=0)
    publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    original_publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    edition: Mapped[int] = mapped_column('edition', default=1)
    serie_id: Mapped[int] = mapped_column(ForeignKey('serie.id'), nullable=True)
    serie: Mapped['SerieModel'] = relationship(foreign_keys=[serie_id], lazy='selectin')
    language_id: Mapped[str] = mapped_column(ForeignKey('language.id'), nullable=True)
    language: Mapped['LanguageModel'] = relationship(foreign_keys=[language_id], lazy='selectin')
    # # cover
    volume: Mapped[int] = mapped_column('volume', default=1)
    publisher_id: Mapped[int] = mapped_column(ForeignKey('publisher.id'), nullable=True)
    publisher: Mapped['PublisherModel'] = relationship(foreign_keys=[publisher_id], lazy='selectin')
    # authors
    main_author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    main_author: Mapped['AuthorModel'] = relationship(foreign_keys=[main_author_id], lazy='selectin')
    collection_id: Mapped[int] = mapped_column(ForeignKey('collection.id'))
    collection: Mapped['CollectionModel'] = relationship(foreign_keys=[collection_id], lazy='selectin')
    format: Mapped[str] = mapped_column('format', nullable=True)
    type: Mapped[str] = mapped_column('type', nullable=True)
    last_status_id: Mapped[str] = mapped_column(ForeignKey('status.id'))
    last_status: Mapped['StatusModel'] = relationship(foreign_keys=[last_status_id], lazy='selectin')
    last_status_date: Mapped[datetime.date] = mapped_column(nullable=True)

    cover_price: Mapped[float] = mapped_column('cover_price', default=0)
    paid_price: Mapped[float] = mapped_column('paid_price', default=0)

    dimensions: Mapped[str] = mapped_column('dimensions', nullable=True)
    height: Mapped[float] = mapped_column('height', nullable=True)
    width: Mapped[float] = mapped_column('width', nullable=True)
    thickness: Mapped[float] = mapped_column('thickness', nullable=True)

    summary: Mapped[str] = mapped_column('summary', nullable=True)
    observation: Mapped[str] = mapped_column('observation', nullable=True)

    origin: Mapped[str] = mapped_column('origin', default='SYSTEM')

    cover: Mapped[str] = mapped_column('cover', nullable=True)

    # Relations
    authors: Mapped[list['AuthorModel']] = relationship(secondary='item_author', back_populates='items', lazy='selectin')


class ItemAuthorModel(SQLModel):
    __tablename__ = "item_author"

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'), primary_key=True)
    is_main: Mapped[bool] = mapped_column('is_main', default=True)
    is_translator: Mapped[bool] = mapped_column('is_translator', default=False)
