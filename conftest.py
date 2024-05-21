import asyncio

import pytest
import pytest_asyncio
from alembic.config import Config
from httpx import AsyncClient
from starlette.testclient import TestClient

from backend.database import test_sessionmanager
from main import app
from backend.database import db_session
from managers.core import LanguageManager
from managers.reading import ReadingDataManager
from models import ReadingModel, LanguageModel
from models.base import Base


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def create_test_session():
    async with test_sessionmanager.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with test_sessionmanager.session() as session:
        yield session


@pytest_asyncio.fixture(scope='function', autouse=True)
def override_db_session(create_test_session):
    """
    Overrides the database session, in this case using test_sessionmanager.
    In session end it rolls back all database operations.
    """
    app.dependency_overrides[db_session] = lambda: create_test_session


@pytest_asyncio.fixture(scope='function', autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


#### Create all necessary data in database ####
@pytest_asyncio.fixture
async def create_languages(create_test_session):
    language_list = []

    language = LanguageModel(id='EN', name='English', code='EN')
    language_1 = await LanguageManager(session=create_test_session).create_language(language)

    language = LanguageModel(id='PT', name='Portuguese', code='PT')
    language_2 = await LanguageManager(session=create_test_session).create_language(language)

    language_list.append(language_1)
    language_list.append(language_2)

    return language_list
