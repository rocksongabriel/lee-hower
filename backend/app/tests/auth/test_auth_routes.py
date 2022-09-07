from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_login_user(create_authorized_user, client: TestClient, app: FastAPI) -> None:

    login_cred = {
        "username": create_authorized_user["email"],
        "password": create_authorized_user["password"],
    }

    res = client.post(
        app.url_path_for("users:login-email-and-password"), data=login_cred
    )

    assert res.status_code == 200
