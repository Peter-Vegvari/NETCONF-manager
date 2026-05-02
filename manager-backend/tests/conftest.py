import pytest
from fastapi.testclient import TestClient

from app.core.config import settings, test_settings
from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def connected_client(client: TestClient):
    """Client already connected to the notconf container."""
    response = client.post(
        f"{settings.API_V1_STR}/connect",
        json={
            "host": test_settings.NOTCONF_HOST,
            "port": test_settings.NOTCONF_PORT,
            "user_name": test_settings.NOTCONF_USER,
            "password": test_settings.NOTCONF_PASSWORD,
        },
    )
    assert response.status_code == 200
    yield client
    client.delete(f"{settings.API_V1_STR}/connect")
