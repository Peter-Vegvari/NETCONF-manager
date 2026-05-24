import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.config import settings


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def connected_client(client: TestClient):
    """Client connected to a NETCONF device."""
    response = client.post(
        f"{settings.API_V1_STR}/connect",
        json={
            "host": settings.NOTCONF_HOST,
            "port": settings.NOTCONF_PORT,
            "user_name": settings.NOTCONF_USER,
            "password": settings.NOTCONF_PASSWORD,
        },
    )
    assert response.status_code == 204, f"Failed to connect: {response.text}"
    yield client
    client.delete(f"{settings.API_V1_STR}/connect")
