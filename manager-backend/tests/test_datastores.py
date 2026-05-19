from fastapi.testclient import TestClient

from tests.config import settings


class TestLock:
    def test_lock_running(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/running/lock"
        )
        assert response.status_code == 200
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/datastore/running/lock")

    def test_lock_candidate(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/candidate/lock"
        )
        assert response.status_code == 200
        connected_client.delete(f"{settings.API_V1_STR}/datastore/candidate/lock")

    def test_lock_not_connected(self, client: TestClient):
        response = client.post(f"{settings.API_V1_STR}/datastore/running/lock")
        assert response.status_code == 400

    def test_lock_already_locked(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/datastore/running/lock")
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/running/lock"
        )
        assert response.status_code == 400
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/datastore/running/lock")

    def test_lock_invalid_datastore(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/nonexistent/lock"
        )
        assert response.status_code == 422


class TestUnlock:
    def test_unlock_running(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/datastore/running/lock")
        response = connected_client.delete(
            f"{settings.API_V1_STR}/datastore/running/lock"
        )
        assert response.status_code == 200

    def test_unlock_not_locked(self, connected_client: TestClient):
        response = connected_client.delete(
            f"{settings.API_V1_STR}/datastore/running/lock"
        )
        assert response.status_code == 400

    def test_unlock_not_connected(self, client: TestClient):
        response = client.delete(f"{settings.API_V1_STR}/datastore/running/lock")
        assert response.status_code == 400


class TestGetLockInfo:
    def test_not_locked(self, connected_client: TestClient):
        response = connected_client.get(f"{settings.API_V1_STR}/datastore/running/lock")
        assert response.status_code == 200
        assert response.json() is False

    def test_locked(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/datastore/running/lock")
        response = connected_client.get(f"{settings.API_V1_STR}/datastore/running/lock")
        assert response.status_code == 200
        assert response.json() is True
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/datastore/running/lock")

    def test_not_connected(self, client: TestClient):
        response = client.get(f"{settings.API_V1_STR}/datastore/running/lock")
        assert response.status_code == 400


class TestCopyConfig:
    def test_copy_running_to_candidate(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/running/copy-config/candidate"
        )
        assert response.status_code == 200

    def test_copy_running_to_startup(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/running/copy-config/startup"
        )
        assert response.status_code == 200

    def test_copy_not_connected(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/datastore/running/copy-config/candidate"
        )
        assert response.status_code == 400

    def test_copy_invalid_source(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/datastore/invalid/copy-config/candidate"
        )
        assert response.status_code == 422


class TestDeleteConfig:
    def test_delete_startup(self, connected_client: TestClient):
        response = connected_client.delete(f"{settings.API_V1_STR}/datastore/startup")
        assert response.status_code == 200

    def test_delete_running_fails(self, connected_client: TestClient):
        """Deleting running datastore should fail per NETCONF spec."""
        response = connected_client.delete(f"{settings.API_V1_STR}/datastore/running")
        assert response.status_code == 400

    def test_delete_not_connected(self, client: TestClient):
        response = client.delete(f"{settings.API_V1_STR}/datastore/candidate")
        assert response.status_code == 400
