import asyncio

import pytest
import pytest_asyncio
from alembic.config import Config
from starlette.testclient import TestClient

from backend.database import test_sessionmanager
from main import app
from backend.database import db_session
from managers.reading import ReadingDataManager
from models import ReadingModel
from models.base import Base


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def create_test_connection():
    async with test_sessionmanager.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with test_sessionmanager.session() as session:
        yield session


@pytest_asyncio.fixture(scope='function', autouse=True)
def override_db_session(create_test_connection):
    """
    Overrides the database session, in this case using test_sessionmanager.
    In session end it rolls back all database operations.
    """
    app.dependency_overrides[db_session] = lambda: create_test_connection


# Create data for tests
@pytest_asyncio.fixture
async def items(create_test_connection):
    new_reading = ReadingModel(
        item_id=10,
    )
    await ReadingDataManager(session=create_test_connection).create_reading(new_reading)
