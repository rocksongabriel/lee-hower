from fastapi.testclient import TestClient


def get_client_and_user_data(clientDataFixture):
    client: TestClient = clientDataFixture["client"]
    user_data = clientDataFixture["user_data"]

    return client, user_data
