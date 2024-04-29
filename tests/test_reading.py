from fastapi import status
from starlette.testclient import TestClient

from main import app

# client = TestClient(app)


def test_get_reading(client):
    param = {
        'itemId': 1
    }
    response = client.get("/reading", params=param)
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['success'] is True

    assert 'item_title' in response_json
    assert 'quantity' in response_json
    assert 'readings' in response_json

    # Check types from response
    assert type(response_json['quantity']) is int
    assert type(response_json['readings']) is list


def test_create_reading(client):
    # TODO: item title does not return while creating a reading
    params = {
        "itemId": 4,
        "startDate": "2024-04-25"
    }
    response = client.post("/reading", json=params)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert response_json['success'] is True
    assert 'reading' in response_json
