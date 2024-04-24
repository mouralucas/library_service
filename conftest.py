import pytest
from alembic.config import Config
from starlette.testclient import TestClient

from backend.database import test_sessionmanager
from main import app
from backend.database import db_session


@pytest.fixture(scope='session', autouse=True)
def client():
    async def override_db_session():
        async with test_sessionmanager.session() as session:
            yield session

    app.dependency_overrides[db_session] = override_db_session

    with TestClient(app) as client:
        yield client
