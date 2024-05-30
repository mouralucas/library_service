import datetime
import uuid
from typing import (
    Any,
    Dict,
    List,
)

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class SQLModel(Base):
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column('id', primary_key=True, default=uuid.uuid4)
    active: Mapped[bool] = mapped_column('status', default=True)
    created_at: Mapped[datetime.datetime] = mapped_column('created_at', default=datetime.datetime.utcnow())
    edited_at: Mapped[datetime.datetime] = mapped_column('edited_at', nullable=True)
    deleted_at: Mapped[datetime.datetime] = mapped_column('deleted_at', nullable=True)

    @classmethod
    def schema(cls) -> str:
        """Return name of database schema the model refers to."""

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """Return name of the table the model refers to."""

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        return cls.__mapper__.selectable.c.keys()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to a dictionary."""

        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict

    @classmethod
    def gather_metadata(cls) -> MetaData:
        """Gather metadata from all subclasses."""
        metadata = MetaData()
        for subclass in cls.__subclasses__():
            Table(subclass.__tablename__, metadata, autoload_with=subclass.metadata.bind)
        return metadata
