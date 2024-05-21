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