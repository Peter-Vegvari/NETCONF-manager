import time
from typing import Any

from fastapi.testclient import TestClient

from tests.config import settings


class TestGetModules:
    def test_returns_list(self, connected_client: TestClient):
        response = connected_client.get(f"{settings.API_V1_STR}/modules/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_modules_have_name_and_status(self, connected_client: TestClient):
        response = connected_client.get(f"{settings.API_V1_STR}/modules/")
        for module in response.json():
            assert "name" in module
            assert "status" in module

    def test_not_connected_returns_empty(self, client: TestClient):
        response = client.get(f"{settings.API_V1_STR}/modules/")
        assert response.status_code == 200
        assert response.json() == []

    def test_unreachable_host_returns_200(self, client: TestClient):
        """When not connected, should return 200 with local modules only."""
        response = client.get(f"{settings.API_V1_STR}/modules/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestDownloadModule:
    def test_download_single_module(self, connected_client: TestClient):
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        assert len(modules) > 0
        module_name = modules[0]["name"]

        response = connected_client.post(
            f"{settings.API_V1_STR}/modules/{module_name}/download"
        )
        assert response.status_code == 204

        modules_after = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        downloaded = next(m for m in modules_after if m["name"] == module_name)
        assert downloaded["status"] == "local"

        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/modules/{module_name}")


class TestDownloadAllModules:
    def test_download_all(self, connected_client: TestClient):
        response = connected_client.post(f"{settings.API_V1_STR}/modules/download-all")
        assert response.status_code == 204
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/modules/")

    def test_not_connected_returns_400(self, client: TestClient):
        response = client.post(f"{settings.API_V1_STR}/modules/download-all")
        assert response.status_code == 400


class TestDownloadModuleEdgeCases:
    def test_download_not_connected(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/modules/ietf-interfaces/download"
        )
        assert response.status_code == 400

    def test_download_nonexistent_module(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/modules/nonexistent-module-xyz/download"
        )
        assert response.status_code == 400


class TestDeleteModule:
    def test_delete_downloaded_module(self, connected_client: TestClient):
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        module_name = modules[0]["name"]
        connected_client.post(f"{settings.API_V1_STR}/modules/{module_name}/download")

        response = connected_client.delete(
            f"{settings.API_V1_STR}/modules/{module_name}"
        )
        assert response.status_code == 204

    def test_delete_nonexistent_module(self, client: TestClient):
        response = client.delete(f"{settings.API_V1_STR}/modules/nonexistent-module")
        assert response.status_code == 404


class TestDeleteAllModules:
    def test_delete_all(self, connected_client: TestClient):
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        module_name = modules[0]["name"]
        connected_client.post(f"{settings.API_V1_STR}/modules/{module_name}/download")

        response = connected_client.delete(f"{settings.API_V1_STR}/modules/")
        assert response.status_code == 204

        modules_after = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        local = [m for m in modules_after if m["status"] == "local"]
        assert local == []


class TestGetModuleSchema:
    def test_schema_after_download_all(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/modules/download-all")

        response = connected_client.get(
            f"{settings.API_V1_STR}/modules/ietf-interfaces/schema"
        )
        assert response.status_code == 200
        schema = response.json()
        assert schema["children"] is not None
        assert any(
            key.startswith("ietf-interfaces:") for key in schema["children"].keys()
        )
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/modules/")

    def test_schema_not_downloaded(self, client: TestClient):
        response = client.get(
            f"{settings.API_V1_STR}/modules/nonexistent-module/schema"
        )
        assert response.status_code == 404


class TestGetData:
    @staticmethod
    def _wait_for_data(
        client: TestClient, url: str, key: str, retries: int = 5, delay: float = 2
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for _ in range(retries):
            resp = client.get(url)
            assert resp.status_code == 200
            data = resp.json()
            if key in data:
                return data
            time.sleep(delay)
        return data

    def test_get_module_data_auto(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/modules/download-all")
        data = self._wait_for_data(
            connected_client,
            f"{settings.API_V1_STR}/datastore/running/ietf-interfaces/data",
            "ietf-interfaces:interfaces",
        )
        assert "ietf-interfaces:interfaces" in data
        # Cleanup
        connected_client.delete(f"{settings.API_V1_STR}/modules/")

    def test_get_module_data_not_connected(self, client: TestClient):
        response = client.get(
            f"{settings.API_V1_STR}/datastore/running/ietf-interfaces/data"
        )
        assert response.status_code == 400

    def test_get_data_interfaces(self, connected_client: TestClient):
        connected_client.post(f"{settings.API_V1_STR}/modules/download-all")
        data = self._wait_for_data(
            connected_client,
            f"{settings.API_V1_STR}/datastore/running/ietf-interfaces/data/interfaces",
            "ietf-interfaces:interfaces",
        )
        assert "ietf-interfaces:interfaces" in data
        interfaces = data["ietf-interfaces:interfaces"]["interface"]
        names = [i["name"] for i in interfaces]
        assert "GigabitEthernet0/0/0" in names
        assert "GigabitEthernet0/0/1" in names

    def test_get_data_not_connected(self, client: TestClient):
        response = client.get(
            f"{settings.API_V1_STR}/datastore/running/ietf-interfaces/data/interfaces"
        )
        assert response.status_code == 400
