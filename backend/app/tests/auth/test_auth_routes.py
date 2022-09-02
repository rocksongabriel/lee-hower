from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest


@pytest.fixture()
def test_user(client: TestClient):
    """
    Create and return a new user object
    """
    user_data = {"email": "testuser@gmail.com", "password": "testpass1234"}

    res = client.post("/users/register", json=user_data)

    new_data = res.json()
    new_data["password"] = user_data["password"]

    return new_data


def test_login_user(test_user, client: TestClient, app: FastAPI) -> None:

    login_cred = {
        "username": test_user["email"],
        "password": test_user["password"],
    }

    res = client.post(
        app.url_path_for("users:login-email-and-password"), data=login_cred
    )

    assert res.status_code == 200
