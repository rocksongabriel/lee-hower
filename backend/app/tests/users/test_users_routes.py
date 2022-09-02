from fastapi.testclient import TestClient

from app.users.schemas import UserRead


def test_register_user(client: TestClient) -> None:
    data = {"email": "testuser1@gmail.com", "password": "testpass1234"}

    res = client.post("/users/register", json=data)

    new_user = UserRead(**res.json()).dict()

    assert res.status_code == 201
    assert "id" in new_user
    assert "password" not in new_user
    assert data["email"] == new_user["email"]
