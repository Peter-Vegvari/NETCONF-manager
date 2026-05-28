from typing import Any, cast

import jsondiff
from fastapi import APIRouter, HTTPException, Response, status

import app.dependencies
from app.models import DataStore, EditConfigRequest
from app.services import datastore_service, module_service

datastore_router = APIRouter(prefix="/datastore", tags=["datastore"])


def _strip_namespace(key: str) -> str:
    return key.rpartition(":")[2] or key


@datastore_router.post(
    "/{source}/copy-config/{target}",
    operation_id="copyConfigTo",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def copy_config(source: DataStore, target: DataStore) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.copy_config(source, target)
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@datastore_router.delete(
    "/{data_store}",
    operation_id="deleteConfig",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_config(data_store: DataStore) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.delete_config(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@datastore_router.post(
    "/{data_store}/lock",
    operation_id="lockDatastore",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def lock(data_store: DataStore) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.lock(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@datastore_router.delete(
    "/{data_store}/lock",
    operation_id="unlockDatastore",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unlock(data_store: DataStore) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.unlock(data_store)
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@datastore_router.get("/{data_store}/lock", operation_id="getLock")
async def get_lock_info(data_store: DataStore) -> bool:
    app.dependencies.connection_manager.check_connected()
    return datastore_service.is_locked(data_store)


@datastore_router.get("/{data_store}/{module_name}/data", operation_id="getModuleData")
async def get_module_data(data_store: DataStore, module_name: str) -> dict[str, Any]:
    app.dependencies.connection_manager.check_connected()
    schema = module_service.get_module_schema(module_name)
    if not schema.children:
        raise HTTPException(404, "No schema available")
    first_key = next(iter(schema.children))
    return module_service.get_data(module_name, data_store, _strip_namespace(first_key))


@datastore_router.get(
    "/{data_store}/{module_name}/data/{path:path}", operation_id="getData"
)
async def get_data(
    data_store: DataStore, module_name: str, path: str
) -> dict[str, Any]:
    app.dependencies.connection_manager.check_connected()
    return module_service.get_data(module_name, data_store, path)


@datastore_router.patch(
    "/{data_store}",
    operation_id="editConfig",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def edit_config(data_store: DataStore, body: EditConfigRequest) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.edit_config(
            data_store, body.module_name, body.path, body.value
        )
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@datastore_router.get(
    "/staged/{module_name}",
    operation_id="get_staged",
)
async def get_staged(module_name: str) -> dict[str, Any]:
    app.dependencies.connection_manager.check_connected()
    schema = module_service.get_module_schema(module_name)
    if not schema.children:
        raise HTTPException(404, "No schema available")
    first_key = next(iter(schema.children))
    path = _strip_namespace(first_key)

    source = module_service.get_data(module_name, DataStore.RUNNING, path)
    destination = module_service.get_data(module_name, DataStore.CANDIDATE, path)

    return cast(dict[str, Any], jsondiff.diff(source, destination, marshal=True))


@datastore_router.post(
    "/commit",
    operation_id="commit",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def commit() -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        datastore_service.commit()
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
