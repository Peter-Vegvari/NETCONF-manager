from fastapi.testclient import TestClient

from app.core.config import settings


def test_connect(client: TestClient):
    from app.core.config import test_settings

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


def test_disconnect(connected_client: TestClient):
    response = connected_client.delete(f"{settings.API_V1_STR}/connect")
    assert response.status_code == 200


def test_get_modules(connected_client: TestClient):
    response = connected_client.get(f"{settings.API_V1_STR}/modules/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
