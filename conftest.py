import pytest
from alembic.config import Config
from starlette.testclient import TestClient

from backend.database import test_sessionmanager
from main import app
from backend.database import db_session


@pytest.fixture(scope='session', autouse=True)
def client():
    async def override_db_session():
        """
            Overrides the database session, in this case using test_sessionmanager.
            In session end it rolls back all database operations.
        """
        async with test_sessionmanager.session() as session:
            try:
                yield session
            finally:
                await session.rollback()

    app.dependency_overrides[db_session] = override_db_session

    with TestClient(app) as client:
        yield client
