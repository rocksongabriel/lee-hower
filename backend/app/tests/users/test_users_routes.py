import json

from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    data = {"email": "testuser1@gmail.com", "password": "testpass1234"}

    response = client.post("/users/register", json.dumps(data))

    assert response.status_code == 201
