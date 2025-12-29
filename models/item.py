import datetime
import uuid

from rolf_common.models import SQLModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.core import AuthorModel


class ItemModel(SQLModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    owner_id: Mapped[uuid.UUID]
    isbn: Mapped[str] = mapped_column("isbn", nullable=True)
    isbn10: Mapped[str] = mapped_column("isbn10", nullable=True)

    title: Mapped[str] = mapped_column(index=True)
    title_original: Mapped[str] = mapped_column("title_original", nullable=True)
    subtitle: Mapped[str] = mapped_column("subtitle", nullable=True)
    subtitle_original: Mapped[str] = mapped_column("subtitle_original", nullable=True)
    pages: Mapped[int] = mapped_column("pages", default=0)
    publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    original_publication_date: Mapped[datetime.date] = mapped_column(nullable=True)
    edition: Mapped[int] = mapped_column("edition", default=1)
    serie_id: Mapped[int] = mapped_column(ForeignKey("serie.id"), nullable=True)
    serie: Mapped["SerieModel"] = relationship(  # noqa: F821
        foreign_keys=[serie_id], lazy="noload"
    )  # noqa: F821
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    language: Mapped["LanguageModel"] = relationship(  # noqa: F821
        foreign_keys=[language_id], lazy="noload"
    )

    volume: Mapped[int] = mapped_column("volume", default=1)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"), nullable=True)
    publisher: Mapped["PublisherModel"] = relationship(  # noqa: F821
        foreign_keys=[publisher_id], lazy="noload"
    )
    # authors
    main_author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    main_author: Mapped["AuthorModel"] = relationship(  # noqa: F821
        foreign_keys=[main_author_id], lazy="noload"
    )

    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    collection: Mapped["CollectionModel"] = relationship(  # noqa: F821
        foreign_keys=[collection_id], lazy="noload"
    )
    format: Mapped[str] = mapped_column("format", nullable=True)
    type: Mapped[str] = mapped_column("type", nullable=True)
    last_status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    last_status: Mapped["StatusModel"] = relationship(  # noqa: F821
        foreign_keys=[last_status_id], lazy="noload"
    )
    last_status_date: Mapped[datetime.date] = mapped_column(nullable=True)

    cover_price: Mapped[float] = mapped_column("cover_price", default=0)
    paid_price: Mapped[float] = mapped_column("paid_price", default=0)

    dimensions: Mapped[str] = mapped_column("dimensions", nullable=True)
    height: Mapped[float] = mapped_column("height", nullable=True)
    width: Mapped[float] = mapped_column("width", nullable=True)
    thickness: Mapped[float] = mapped_column("thickness", nullable=True)

    summary: Mapped[str] = mapped_column("summary", nullable=True)  # continue here
    observation: Mapped[str] = mapped_column(
        "observation", nullable=True
    )  # go to user item

    origin: Mapped[str] = mapped_column("origin", default="SYSTEM")

    cover: Mapped[str] = mapped_column("cover", nullable=True)

    # Relations
    authors: Mapped[list["AuthorModel"]] = relationship(  # noqa: F821
        "AuthorModel", secondary="item_author", lazy="noload", viewonly=True
    )
    status: Mapped[list["StatusModel"]] = relationship(  # noqa: F821
        "StatusModel", secondary="item_status", lazy="noload", viewonly=True
    )  # go to user item


class ItemAuthorModel(SQLModel):
    __tablename__ = "item_author"

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped["ItemModel"] = relationship(foreign_keys=[item_id], lazy="selectin")

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["AuthorModel"] = relationship(  # noqa: F821
        foreign_keys=[author_id], lazy="selectin"
    )

    is_main: Mapped[bool] = mapped_column("is_main", default=True)
    is_translator: Mapped[bool] = mapped_column("is_translator", default=False)


class ItemStatusModel(SQLModel):
    __tablename__ = "item_status"

    status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    status: Mapped["StatusModel"] = relationship(  # noqa: F821
        foreign_keys=[status_id], lazy="selectin"
    )

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped["ItemModel"] = relationship(foreign_keys=[item_id], lazy="selectin")

    date: Mapped[datetime.date] = mapped_column("date")


####### Item V2 #######
class ItemMetadataModel(SQLModel):
    __tablename__ = "item_metadata"

    original_language_id: Mapped[str] = mapped_column(
        ForeignKey("language.id"), nullable=True
    )
    original_language: Mapped["LanguageModel"] = relationship(  # noqa: F821
        foreign_keys=[original_language_id], lazy="noload"
    )
    type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("item_type.id"), doc="Book, manga, HQ"
    )
    main_author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    main_author: Mapped["AuthorModel"] = relationship(
        foreign_keys=[main_author_id], lazy="noload"
    )

    # Relations
    authors: Mapped[list["AuthorModel"]] = relationship(
        "AuthorModel", secondary="item_metadata_author", lazy="noload", viewonly=True
    )


class ItemMetadataAuthorModel(SQLModel):
    __tablename__ = "item_metadata_author"

    item_metadata_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("item_metadata.id"))
    item_metadata: Mapped["ItemMetadataModel"] = relationship(
        foreign_keys=[item_metadata_id], lazy="selectin"
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["AuthorModel"] = relationship(  # noqa: F821
        foreign_keys=[author_id], lazy="selectin"
    )

    is_main: Mapped[bool] = mapped_column("is_main", default=True)
    position: Mapped[int] = mapped_column("position", default=0)


class ItemEditionModel(SQLModel):
    __tablename__ = "item_edition"

    item_metadata_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("item_metadata.id"))
    title: Mapped[str] = mapped_column("title")
    subtitle: Mapped[str | None] = mapped_column("subtitle", nullable=True)
    isbn: Mapped[str | None] = mapped_column("isbn", nullable=True)
    pages: Mapped[int | None] = mapped_column("pages", nullable=True)
    format_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("item_format.id"), nullable=True
    )
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"), nullable=True)
    published_date: Mapped[datetime.date] = mapped_column(
        "published_date", nullable=True
    )
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    language: Mapped["LanguageModel"] = relationship(  # noqa: F821
        foreign_keys=[language_id], lazy="noload"
    )
    summary: Mapped[str] = mapped_column("summary", nullable=True)
    cover_price: Mapped[float] = mapped_column("cover_price", default=0)

    # series and collections here?


class ItemEditionUserModel(SQLModel):
    __tablename__ = "user_item_edition"

    item_edition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("item_edition.id"))
    user_id: Mapped[uuid.UUID] = mapped_column("user_id")
    notes: Mapped[str] = mapped_column("notes", nullable=True)
    last_status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    last_status: Mapped["StatusModel"] = relationship(  # noqa: F821
        foreign_keys=[last_status_id], lazy="noload"
    )
    last_status_date: Mapped[datetime.date] = mapped_column(nullable=True)

    # Relations
    status: Mapped[list["StatusModel"]] = relationship(  # noqa: F821
        "StatusModel",
        secondary="user_item_edition_status",
        lazy="noload",
        viewonly=True,
    )


class UserItemEditionStatusModel(SQLModel):
    __tablename__ = "user_item_edition_status"

    status_id: Mapped[str] = mapped_column(ForeignKey("status.id"))
    status: Mapped["StatusModel"] = relationship(  # noqa: F821
        foreign_keys=[status_id], lazy="selectin"
    )

    user_edition_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_item_edition.id")
    )
    user_edition: Mapped["ItemEditionUserModel"] = relationship(  # noqa: F821
        foreign_keys=[user_edition_id], lazy="selectin"
    )

    date: Mapped[datetime.date] = mapped_column("date")
