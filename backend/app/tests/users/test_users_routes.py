from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.tests.conftest import create_single_user
from app.tests.utils import get_client_and_user_data
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
    client, user_data = get_client_and_user_data(authDataClient)

    url = app.url_path_for("users:get-users")
    res = client.get(url)

    user_data.pop("password")

    users: list[UserRead] = res.json()

    assert res.status_code == 200
    assert len(users) == 3
    assert user_data in users


def test_get_user(authDataClient, app: FastAPI) -> None:
    client, user_data = get_client_and_user_data(authDataClient)

    url = app.url_path_for("users:get-user", uuid=user_data["id"])
    res = client.get(url)

    print(user_data)
    print("----------------------------------------------------")
    print(res.json())

    res_data = res.json()

    assert res.status_code == 200
    assert "id" in res_data
    assert "first_name" in res_data
    assert "last_name" in res_data
    assert "is_active" in res_data
    assert res_data["is_active"] == True
    assert "created" in res_data
    assert "password" not in res_data


def test_update_user(authDataClient, app: FastAPI) -> None:
    client, user_data = get_client_and_user_data(authDataClient)

    new_user_data = {
        "first_name": "Gabriel",
        "last_name": "Rockson",
        "email": user_data["email"],
        "is_active": user_data["is_active"],
        "created": user_data["created"],
    }

    url = app.url_path_for("users:update-user", uuid=user_data["id"])
    res = client.put(url, json=new_user_data)

    res_data = res.json()

    assert res.status_code == 200
    assert res_data["first_name"] == new_user_data["first_name"]
    assert res_data["last_name"] == new_user_data["last_name"]


def test_delete_user(authDataClient, app: FastAPI) -> None:
    client, user_data = get_client_and_user_data(authDataClient)

    url = app.url_path_for("users:delete-user", uuid=user_data["id"])
    res = client.delete(url)

    assert res.status_code == 204
