from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest


def test_login_user(
    create_single_user, client: TestClient, app: FastAPI
) -> None:

    login_cred = {
        "username": create_single_user["email"],
        "password": create_single_user["password"],
    }

    res = client.post(
        app.url_path_for("users:login-email-and-password"), data=login_cred
    )

    assert res.status_code == 200
