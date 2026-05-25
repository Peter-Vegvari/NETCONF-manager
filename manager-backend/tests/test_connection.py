from fastapi.testclient import TestClient

from app.models import Connection
from tests.config import settings

_connection = Connection(
    host=settings.NOTCONF_HOST,
    port=settings.NOTCONF_PORT,
    user_name=settings.NOTCONF_USER,
    password=settings.NOTCONF_PASSWORD,
)


class TestConnect:
    def test_connect_success(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_dump(),
        )
        assert response.status_code == 204

    def test_connect_invalid_host(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=Connection(
                host="invalid-host", port=830, user_name="admin", password="admin"
            ).model_dump(),
        )
        assert response.status_code == 400

    def test_connect_invalid_port(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_copy(update={"port": 9999}).model_dump(),
        )
        assert response.status_code == 400

    def test_connect_invalid_credentials(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_copy(
                update={"user_name": "wrong", "password": "wrong"}
            ).model_dump(),
        )
        assert response.status_code == 400

    def test_connect_missing_fields(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json={"host": settings.NOTCONF_HOST},
        )
        assert response.status_code == 422

    def test_connect_empty_body(self, client: TestClient):
        response = client.post(f"{settings.API_V1_STR}/connect", json={})
        assert response.status_code == 422


class TestConnectIdempotency:
    def test_connect_twice_same_credentials(self, client: TestClient):
        """Posting connect twice with same credentials should succeed both times."""
        for _ in range(2):
            response = client.post(
                f"{settings.API_V1_STR}/connect",
                json=_connection.model_dump(),
            )
            assert response.status_code == 204

    def test_connect_twice_different_credentials(self, client: TestClient):
        """Connecting with different credentials after already connected."""
        client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_dump(),
        )
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_copy(
                update={"user_name": "wrong", "password": "wrong"}
            ).model_dump(),
        )
        assert response.status_code == 400

    def test_connect_disconnect_connect(self, client: TestClient):
        """Reconnecting after disconnect should work."""
        client.post(f"{settings.API_V1_STR}/connect", json=_connection.model_dump())
        client.delete(f"{settings.API_V1_STR}/connect")
        response = client.post(
            f"{settings.API_V1_STR}/connect",
            json=_connection.model_dump(),
        )
        assert response.status_code == 204

    def test_connect_then_disconnect_then_disconnect(self, client: TestClient):
        """Disconnecting twice should be safe (idempotent)."""
        client.post(f"{settings.API_V1_STR}/connect", json=_connection.model_dump())
        client.delete(f"{settings.API_V1_STR}/connect")
        response = client.delete(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200

    def test_rapid_connect_calls(self, client: TestClient):
        """Multiple rapid connect calls should not cause server errors."""
        for _ in range(5):
            response = client.post(
                f"{settings.API_V1_STR}/connect",
                json=_connection.model_dump(),
            )
            assert response.status_code == 204


class TestDisconnect:
    def test_disconnect_success(self, connected_client: TestClient):
        response = connected_client.delete(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200
        assert response.json() == []

    def test_disconnect_when_not_connected(self, client: TestClient):
        response = client.delete(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200
        assert response.json() == []


class TestConnectionStatus:
    def test_status_not_connected(self, client: TestClient):
        response = client.get(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200
        assert response.json() is False

    def test_status_connected(self, connected_client: TestClient):
        response = connected_client.get(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200
        assert response.json() is True

    def test_status_after_disconnect(self, connected_client: TestClient):
        connected_client.delete(f"{settings.API_V1_STR}/connect")
        response = connected_client.get(f"{settings.API_V1_STR}/connect")
        assert response.status_code == 200
        assert response.json() is False
