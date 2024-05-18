import asyncio

import pytest
from alembic.config import Config
from starlette.testclient import TestClient

from backend.database import test_sessionmanager
from main import app
from backend.database import db_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
def override_db_session():
    """
    Overrides the database session, in this case using test_sessionmanager.
    In session end it rolls back all database operations.
    """

    async def _override_db_session():
        async with test_sessionmanager.session() as session:

            try:
                transaction = session.begin_nested()
                yield session
            finally:
                transaction.rollback()
                await session.rollback()

    app.dependency_overrides[db_session] = _override_db_session


# @pytest.fixture(scope='session')
# def client():
#     with TestClient(app) as c:
#         yield c
