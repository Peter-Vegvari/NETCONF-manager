from typing import Any

from fastapi import APIRouter, HTTPException

import app.dependencies
from app.models.datastore import DataStore, EditConfigRequest
from app.services import datastore_service, module_service

datastore_router = APIRouter(prefix="/datastore", tags=["datastore"])


def _check_connected():
    if app.dependencies.connection_manager.session is None:
        raise HTTPException(400, "Not connected")


@datastore_router.post("/{source}/copy-config/{target}", operation_id="copyConfigTo")
async def copy_config(source: DataStore, target: DataStore) -> str:
    _check_connected()
    try:
        return datastore_service.copy_config(source, target)
    except Exception as e:
        raise HTTPException(400, str(e))


@datastore_router.delete("/{data_store}", operation_id="deleteConfig")
async def delete_config(data_store: DataStore) -> str:
    _check_connected()
    try:
        return datastore_service.delete_config(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))


@datastore_router.post("/{data_store}/lock", operation_id="lockDatastore")
async def lock(data_store: DataStore) -> str:
    _check_connected()
    try:
        return datastore_service.lock(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))


@datastore_router.delete("/{data_store}/lock", operation_id="unlockDatastore")
async def unlock(data_store: DataStore) -> str:
    _check_connected()
    try:
        return datastore_service.unlock(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))


@datastore_router.get("/{data_store}/lock", operation_id="getLock")
async def get_lock_info(data_store: DataStore) -> bool:
    _check_connected()
    return datastore_service.is_locked(data_store)


@datastore_router.get("/{data_store}/{module_name}/data", operation_id="getModuleData")
async def get_module_data(module_name: str, data_store: DataStore) -> dict[str, Any]:
    _check_connected()
    schema = module_service.get_module_schema(module_name)
    if not schema.children:
        raise HTTPException(404, "No schema available")
    first_key = next(iter(schema.children))
    return module_service.get_data(
        module_name, data_store, first_key.rpartition(":")[2] or first_key
    )


@datastore_router.get(
    "/{data_store}/{module_name}/data/{path:path}", operation_id="getData"
)
async def get_data(
    module_name: str, data_store: DataStore, path: str
) -> dict[str, Any]:
    _check_connected()
    return module_service.get_data(module_name, data_store, path)


@datastore_router.post("/{data_store}/edit-config", operation_id="editConfig")
async def edit_config(data_store: DataStore, body: EditConfigRequest) -> str:
    _check_connected()
    try:
        return datastore_service.edit_config(
            data_store, body.module_name, body.path, body.value
        )
    except Exception as e:
        raise HTTPException(400, str(e))
