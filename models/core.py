from models.base import SQLModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StatusModel(SQLModel):
    __tablename__ = "status"
    __table_args__ = {"schema": "public"}

    id: Mapped[str]
    name: Mapped[str]
    description: Mapped[str]
    order: Mapped[int]
    type: Mapped[str]