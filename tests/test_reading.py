# client = TestClient(app)

def test_reading(client):
    param = {
        'itemId': 1
    }
    response = client.get("/reading", params=param)
    assert response.status_code == 200
