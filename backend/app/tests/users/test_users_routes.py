from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.tests.conftest import create_single_user

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


def test_get_users(authDataClient, create_multiple_users, app: FastAPI) -> None:
    client: TestClient = authDataClient["client"]
    user_data = authDataClient["user_data"]

    url = app.url_path_for("users:get-users")

    res = client.get(url)

    users: list[UserRead] = res.json()

    assert res.status_code == 200
    assert len(users) == 3


def test_get_user(authDataClient, app: FastAPI) -> None:
    client: TestClient = authDataClient["client"]
    user_data = authDataClient["user_data"]

    url = app.url_path_for("users:get-user", uuid=user_data["id"])
    res = client.get(url)

    assert res.status_code == 200
    assert "id" in user_data
    assert "first_name" in user_data
    assert "last_name" in user_data
