import uuid
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import LanguageModel
from models.base import SQLModel


class SerieModel(SQLModel):
    __tablename__ = "serie"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    nm_original: Mapped[str] = mapped_column('nm_original')
    description: Mapped[str] = mapped_column('description')
    county_id: Mapped[str] = mapped_column('country_id')


class CollectionModel(SQLModel):
    __tablename__ = "collection"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    description: Mapped[str] = mapped_column('description')


class PublisherModel(SQLModel):
    __tablename__ = "publisher"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    description: Mapped[str] = mapped_column('description')
    county_id: Mapped[str] = mapped_column('country_id')
    parent_id: Mapped[int] = mapped_column('parent_id')


class AuthorModel(SQLModel):
    __tablename__ = "author"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    nm_full: Mapped[str] = mapped_column('nm_full')


class ItemModel(SQLModel):
    # TODO: remove all selectin after tests
    __tablename__ = "item"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    owner_id: Mapped[uuid.UUID]
    isbn_formatted: Mapped[int] = mapped_column('isbn_formatted', nullable=True)
    isbn10_formatted: Mapped[int] = mapped_column('isbn10_formatted', nullable=True)

    title: Mapped[str]
    title_original: Mapped[str] = mapped_column('title_original', nullable=True)
    subtitle: Mapped[str] = mapped_column('subtitle', nullable=True)
    subtitle_original: Mapped[str] = mapped_column('subtitle_original', nullable=True)
    pages: Mapped[int] = mapped_column('pages', default=0)
    published_at: Mapped[datetime.date] = mapped_column('published_at', nullable=True)
    published_original_at: Mapped[datetime.date] = mapped_column('published_original_at', nullable=True)
    edition: Mapped[int] = mapped_column('edition', default=1)
    serie_id: Mapped[int] = mapped_column(ForeignKey('library.serie.id'))
    serie: Mapped['SerieModel'] = relationship(foreign_keys=[serie_id], lazy='selectin')
    language_id: Mapped[str] = mapped_column(ForeignKey('public.language.id'))
    language: Mapped['LanguageModel'] = relationship(foreign_keys=[language_id], lazy='selectin')
    # # cover
    volume: Mapped[int] = mapped_column('volume', default=1)
    publisher_id: Mapped[int] = mapped_column(ForeignKey('library.publisher.id'))
    publisher: Mapped['PublisherModel'] = relationship(foreign_keys=[publisher_id], lazy='selectin')
    # authors
    main_author_id: Mapped[int] = mapped_column(ForeignKey('library.author.id'))
    main_author: Mapped['AuthorModel'] = relationship(foreign_keys=[main_author_id], lazy='selectin')
    collection_id: Mapped[int] = mapped_column(ForeignKey('library.collection.id'))
    collection: Mapped['CollectionModel'] = relationship(foreign_keys=[collection_id], lazy='selectin')
    # format -- create table?
    # type -- create table?
    # status
    # status at
    # log status
    cover_price: Mapped[float] = mapped_column('cover_price', default=0)
    paid_price: Mapped[float] = mapped_column('paid_price', default=0)

    dimensions: Mapped[str] = mapped_column('dimensions', nullable=True)
    height: Mapped[float] = mapped_column('height', nullable=True)
    width: Mapped[float] = mapped_column('width', nullable=True)
    thickness: Mapped[float] = mapped_column('thickness', nullable=True)

    summary: Mapped[str]
    observation: Mapped[str]

    origin: Mapped[str] = mapped_column('origin', default='SYSTEM')
