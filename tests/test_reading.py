from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def setup_function():
    pass


def test_reading():
    param = {
        'item_id': 1
    }
    response = client.get("/reading", params=param)
    assert response.status_code == 200
