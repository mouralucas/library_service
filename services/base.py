from typing import (
    Any,
    List,
    Sequence,
    Type,
)

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.orm import Session


class SessionMixin:
    """Provides instance of database session."""

    def __init__(self, session: Session) -> None:
        self.session = session


class BaseService(SessionMixin):
    """Base class for application services."""
