import datetime

from rolf_common.models import SQLModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StatusModel(SQLModel):
    __tablename__ = "status"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column("description", nullable=True)
    order: Mapped[int] = mapped_column("order", nullable=True)
    type: Mapped[str] = mapped_column("type", nullable=True)

    items: Mapped["ItemModel"] = relationship(
        "ItemModel", secondary="item_status", lazy="noload", viewonly=True
    )  # noqa: F821


class LanguageModel(SQLModel):
    __tablename__ = "language"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(nullable=True)


class CountryModel(SQLModel):
    __tablename__ = "country"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    continent: Mapped[str]
    description: Mapped[str] = mapped_column("description", nullable=True)


class SerieModel(SQLModel):
    __tablename__ = "serie"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    original_name: Mapped[str] = mapped_column("nm_original", nullable=True)
    description: Mapped[str] = mapped_column("description", nullable=True)
    country_id: Mapped[str] = mapped_column("country_id", nullable=True)


class CollectionModel(SQLModel):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    description: Mapped[str] = mapped_column("description", nullable=True)
    # serie_id: Mapped[int] = mapped_column(
    #     ForeignKey("serie.id"),
    #     nullable=True,
    #     doc="The serie id if collection is related to a serie",
    # )


class PublisherModel(SQLModel):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    description: Mapped[str] = mapped_column("description", nullable=True)
    country_id: Mapped[str] = mapped_column("country_id", nullable=True)
    parent_id: Mapped[int] = mapped_column("parent_id", nullable=True)


class AuthorModel(SQLModel):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("name")
    first_name: Mapped[str] = mapped_column("first_name", nullable=True)
    last_name: Mapped[str] = mapped_column("last_name", nullable=True)
    birth_date: Mapped[datetime.date] = mapped_column("birth_date", nullable=True)
    description: Mapped[str] = mapped_column("description", nullable=True)
    country_id: Mapped[str] = mapped_column(ForeignKey("country.id"), nullable=True)
    country: Mapped["CountryModel"] = relationship(
        foreign_keys=[country_id], lazy="noload"
    )
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    language: Mapped["LanguageModel"] = relationship(
        foreign_keys=[language_id], lazy="noload"
    )
    is_translator: Mapped[bool] = mapped_column("is_translator", default=False)

    items: Mapped["ItemModel"] = relationship(
        "ItemModel", secondary="item_author", viewonly=True, lazy="noload"
    )  # noqa: F821
