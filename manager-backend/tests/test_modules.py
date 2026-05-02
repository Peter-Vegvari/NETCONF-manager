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


class TestDownloadModule:
    def test_download_single_module(self, connected_client: TestClient):
        # Get a module name from the remote list
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        assert len(modules) > 0
        module_name = modules[0]["name"]

        response = connected_client.post(
            f"{settings.API_V1_STR}/modules/{module_name}/download"
        )
        assert response.status_code == 200

        # Verify it's now local
        modules_after = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        downloaded = next(m for m in modules_after if m["name"] == module_name)
        assert downloaded["status"] == "local"


class TestDownloadAllModules:
    def test_download_all(self, connected_client: TestClient):
        response = connected_client.post(
            f"{settings.API_V1_STR}/modules/download-all"
        )
        assert response.status_code == 200

    def test_not_connected_returns_400(self, client: TestClient):
        response = client.post(f"{settings.API_V1_STR}/modules/download-all")
        assert response.status_code == 400


class TestDeleteModule:
    def test_delete_downloaded_module(self, connected_client: TestClient):
        # Download one first
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        module_name = modules[0]["name"]
        connected_client.post(f"{settings.API_V1_STR}/modules/{module_name}/download")

        # Delete it
        response = connected_client.delete(
            f"{settings.API_V1_STR}/modules/{module_name}"
        )
        assert response.status_code == 200

    def test_delete_nonexistent_module(self, client: TestClient):
        response = client.delete(f"{settings.API_V1_STR}/modules/nonexistent-module")
        assert response.status_code == 404


class TestDeleteAllModules:
    def test_delete_all(self, connected_client: TestClient):
        # Download one first so there's something to delete
        modules = connected_client.get(f"{settings.API_V1_STR}/modules/").json()
        module_name = modules[0]["name"]
        connected_client.post(f"{settings.API_V1_STR}/modules/{module_name}/download")

        response = connected_client.delete(f"{settings.API_V1_STR}/modules/")
        assert response.status_code == 200

        # Verify no local modules remain
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

    def test_schema_not_downloaded(self, client: TestClient):
        response = client.get(
            f"{settings.API_V1_STR}/modules/nonexistent-module/schema"
        )
        assert response.status_code == 200
        # Returns empty schema node
        assert response.json()["kind"] == ""
