from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.users.schemas import UserRead


@pytest.fixture()
def create_multiple_users(client: TestClient):
    user1_data = {"email": "user1@gmail.com", "password": "testpass1234"}
    user2_data = {"email": "user2@gmail.com", "password": "testpass1234"}

    url = "/users/register"

    client.post(url, json=user1_data)
    client.post(url, json=user2_data)


def test_register_user(client: TestClient) -> None:
    data = {"email": "testuser1@gmail.com", "password": "testpass1234"}

    res = client.post("/users/register", json=data)

    new_user = UserRead(**res.json()).dict()

    assert res.status_code == 201
    assert "id" in new_user
    assert "password" not in new_user
    assert data["email"] == new_user["email"]


def test_get_users(
    authClient: TestClient, create_multiple_users, app: FastAPI
) -> None:
    url = app.url_path_for("users:get-users")

    res = authClient.get(url)

    users: list[UserRead] = res.json()

    assert res.status_code == 200
    assert len(users) == 3


def test_get_user(authClient: TestClient, app: FastAPI) -> None:
    user_id = authClient.headers.get("user_id")
    url = app.url_path_for("users:get-user", uuid=user_id)

    authClient.headers.pop("user_id")
    res = authClient.get(url)

    assert res.status_code == 200
