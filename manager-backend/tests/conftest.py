import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.config import settings


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(
    params=[
        pytest.param(
            {
                "host": settings.NOTCONF_HOST,
                "port": settings.NOTCONF_PORT,
                "user_name": settings.NOTCONF_USER,
                "password": settings.NOTCONF_PASSWORD,
            },
            id="notconf",
        ),
        pytest.param(
            {
                "host": settings.REAL_DEVICE_HOST,
                "port": settings.REAL_DEVICE_PORT,
                "user_name": settings.REAL_DEVICE_USER,
                "password": settings.REAL_DEVICE_PASSWORD,
            },
            id="real_device",
            marks=pytest.mark.real_device,
        ),
    ]
)
def connected_client(client: TestClient, request: pytest.FixtureRequest):
    """Client connected to a NETCONF device."""
    response = client.post(
        f"{settings.API_V1_STR}/connect",
        json=request.param,
    )
    assert response.status_code == 200, f"Failed to connect: {response.text}"
    yield client
    client.delete(f"{settings.API_V1_STR}/connect")
