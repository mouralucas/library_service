from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app

client = TestClient(app)


def setup_function():
    pass


def test_reading(db_session: AsyncSession):
    param = {
        'itemId': 1
    }
    response = client.get("/reading", params=param)
    assert response.status_code == 200
