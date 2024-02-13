from sqlalchemy.ext.asyncio import AsyncSession


class SessionMixin:
    """Provides instance of database session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class BaseService(SessionMixin):
    """Base class for application services."""
