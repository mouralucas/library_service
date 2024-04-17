import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.settings import get_settings
from main import app as actual_app


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    # Run alembic migrations on test DB
    # async with sessionmanager.connect() as connection:
    #     await connection.run_sync(run_migrations)

    yield

    # Teardown
    # await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def transactional_session():
    # TODO: set new env to test database
    engine = create_async_engine(get_settings().TEST_DATABASE.test_dsn)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session
