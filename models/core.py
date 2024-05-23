import datetime

from sqlalchemy import ForeignKey

from models.base import SQLModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StatusModel(SQLModel):
    __tablename__ = "status"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    order: Mapped[int]
    type: Mapped[str]


class LanguageModel(SQLModel):
    __tablename__ = "language"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str]


class CountryModel(SQLModel):
    __tablename__ = "country"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    continent: Mapped[str]
    description: Mapped[str] = mapped_column('description', nullable=True)


class SerieModel(SQLModel):
    __tablename__ = "serie"

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    original_name: Mapped[str] = mapped_column('nm_original', nullable=True)
    description: Mapped[str] = mapped_column('description', nullable=True)
    country_id: Mapped[str] = mapped_column('country_id', nullable=True)


class CollectionModel(SQLModel):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    description: Mapped[str] = mapped_column('description', nullable=True)


class PublisherModel(SQLModel):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name')
    description: Mapped[str] = mapped_column('description', nullable=True)
    country_id: Mapped[str] = mapped_column('country_id', nullable=True)
    parent_id: Mapped[int] = mapped_column('parent_id', nullable=True)


class AuthorModel(SQLModel):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column('name')
    first_name: Mapped[str] = mapped_column('first_name', nullable=True)
    last_name: Mapped[str] = mapped_column('last_name', nullable=True)
    birth_date: Mapped[datetime.date] = mapped_column('birth_date', nullable=True)
    description: Mapped[str] = mapped_column('description', nullable=True)
    country_id: Mapped[str] = mapped_column(ForeignKey('country.id'), nullable=True)
    country: Mapped['CountryModel'] = relationship(foreign_keys=[country_id], lazy='selectin')
    language_id: Mapped[str] = mapped_column(ForeignKey('language.id'), nullable=True)
    language: Mapped['LanguageModel'] = relationship(foreign_keys=[language_id], lazy='selectin')
    is_translator: Mapped[bool] = mapped_column('is_translator', default=False)
