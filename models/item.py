import datetime
import uuid

from rolf_common.models import SQLModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.core import (
    AuthorModel,
    CollectionModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
    StatusModel,
)


# TODO: change possible float fields to decimal
class ItemModel(SQLModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    owner_id: Mapped[uuid.UUID]
    isbn: Mapped[str] = mapped_column("isbn", nullable=True)

    title: Mapped[str] = mapped_column(index=True)
    subtitle: Mapped[str] = mapped_column("subtitle", nullable=True)
    pages: Mapped[int] = mapped_column("pages", default=0)
    publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    # Original publication date may be in the metadata table
    original_publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    edition: Mapped[int] = mapped_column("edition", default=1)
    serie_id: Mapped[int] = mapped_column(ForeignKey("serie.id"), nullable=True)
    serie: Mapped["SerieModel"] = relationship(foreign_keys=[serie_id], lazy="noload")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    language: Mapped["LanguageModel"] = relationship(
        foreign_keys=[language_id], lazy="noload"
    )

    volume: Mapped[int] = mapped_column("volume", default=1)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"), nullable=True)
    publisher: Mapped["PublisherModel"] = relationship(
        foreign_keys=[publisher_id], lazy="noload"
    )
    # authors
    main_author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    main_author: Mapped["AuthorModel"] = relationship(
        foreign_keys=[main_author_id], lazy="noload"
    )

    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    collection: Mapped["CollectionModel"] = relationship(
        foreign_keys=[collection_id], lazy="noload"
    )
    format_id: Mapped[str] = mapped_column("format", nullable=True)
    item_type_id: Mapped[str] = mapped_column("type", nullable=True)
    last_status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    last_status: Mapped["StatusModel"] = relationship(
        foreign_keys=[last_status_id], lazy="noload"
    )
    last_status_date: Mapped[datetime.date] = mapped_column(nullable=True)

    cover_price: Mapped[float] = mapped_column("cover_price", default=0)
    paid_price: Mapped[float] = mapped_column("paid_price", default=0)

    summary: Mapped[str] = mapped_column("summary", nullable=True)  # continue here
    observation: Mapped[str] = mapped_column(
        "observation", nullable=True
    )  # go to user item

    origin: Mapped[str] = mapped_column("origin", default="SYSTEM")

    cover: Mapped[str] = mapped_column("cover", nullable=True)

    # Relations
    authors: Mapped[list["AuthorModel"]] = relationship(
        "AuthorModel", secondary="item_author", lazy="noload", viewonly=True
    )
    status: Mapped[list["StatusModel"]] = relationship(
        "StatusModel", secondary="item_status", lazy="noload", viewonly=True
    )  # go to user item

    location_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("item_location.id"), nullable=True
    )


class ItemAuthorModel(SQLModel):
    __tablename__ = "item_author"

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped["ItemModel"] = relationship(foreign_keys=[item_id], lazy="selectin")

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["AuthorModel"] = relationship(
        foreign_keys=[author_id], lazy="selectin"
    )

    is_main: Mapped[bool] = mapped_column("is_main", default=True)
    is_translator: Mapped[bool] = mapped_column("is_translator", default=False)


class ItemStatusModel(SQLModel):
    __tablename__ = "item_status"

    status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    status: Mapped["StatusModel"] = relationship(
        foreign_keys=[status_id], lazy="selectin"
    )

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped["ItemModel"] = relationship(foreign_keys=[item_id], lazy="selectin")

    date: Mapped[datetime.date] = mapped_column("date")


class ItemLocationModel(SQLModel):
    __tablename__ = "item_location"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column("name", doc="Location name")
    physical_location: Mapped[str] = mapped_column(
        "physical_location", doc="Physical location of the item"
    )
    description: Mapped[str] = mapped_column(
        "description", doc="Additional details about the location", nullable=True
    )
