from typing import Any, Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.db.config import get_db
from app.db.base import Base
from app.main import app as main_app


# Configuration for test Database
settings = get_settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.test_database_username}:{settings.test_database_password}"
    f"@{settings.test_database_host}:{settings.test_database_port}/"
    f"{settings.test_database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)


# Create and drop database tables for each test
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)  # type: ignore
    _app = main_app
    yield _app
    Base.metadata.drop_all(engine)  # type: ignore


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[TestingSessionLocal, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: TestingSessionLocal
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture
    the `get_db` dependency that is injected into routes
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(main_app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def create_single_user(client: TestClient):
    """
    Create and return a new user object
    """
    user_data = {"email": "testuser@gmail.com", "password": "testpass1234"}

    res = client.post("/users/register", json=user_data)

    new_data = res.json()
    new_data["password"] = user_data["password"]

    return new_data


@pytest.fixture(scope="function")
def authClient(client: TestClient, create_single_user, app: FastAPI):
    url = app.url_path_for("users:login-email-and-password")

    login_cred = {
        "username": create_single_user["email"],
        "password": create_single_user["password"],
    }

    res = client.post(url, login_cred)

    access_token = res.json()["access_token"]["token"]

    client.headers["Authorization"] = f"Bearer {access_token}"

    yield client
