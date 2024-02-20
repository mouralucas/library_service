import uuid

from sqlalchemy.orm import Mapped, mapped_column

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
    nm_original: Mapped[str] = mapped_column('nm_original')
    description: Mapped[str] = mapped_column('description')
    county_id: Mapped[str] = mapped_column('country_id')
    parent_id: Mapped[int] = mapped_column('parent_id')


class ItemModel(SQLModel):
    __tablename__ = "item"
    __table_args__ = {"schema": "library"}

    id: Mapped[int] = mapped_column('id', primary_key=True)
    owner_id: Mapped[uuid.UUID]
    isbn_formatted: Mapped[int]
    isbn10_formatted: Mapped[int]

    title: Mapped[str]
    subtitle: Mapped[str]
