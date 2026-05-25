import asyncio

from fastapi import APIRouter, HTTPException, Response, status

import app.dependencies
from app.models import ModuleStatus, ModuleSummary, SchemaNode
from app.services import module_service

module_router = APIRouter(prefix="/modules", tags=["modules"])


@module_router.get("/", operation_id="getModules")
async def get_modules() -> list[ModuleSummary]:
    local = module_service.get_local_modules()
    remote = await asyncio.to_thread(module_service.get_remote_modules)
    seen: set[str] = set()
    result: list[ModuleSummary] = []
    for name in [*local, *remote]:
        if name not in seen:
            seen.add(name)
            status_ = (
                ModuleStatus.LOCAL
                if module_service.is_local(name)
                else ModuleStatus.REMOTE
            )
            result.append(
                ModuleSummary(
                    name=name,
                    status=status_,
                    revision=module_service.get_revision(name),
                )
            )
    return result


@module_router.post(
    "/download-all",
    operation_id="downloadAllModules",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def download_all_modules() -> Response:
    app.dependencies.connection_manager.check_connected()
    module_service.download_all()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@module_router.post(
    "/{module_name}/download",
    operation_id="downloadModule",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def download_module(module_name: str) -> Response:
    app.dependencies.connection_manager.check_connected()
    try:
        module_service.download_module(module_name)
    except Exception as e:
        raise HTTPException(400, str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@module_router.delete(
    "/{module_name}",
    operation_id="deleteModule",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_module(module_name: str) -> Response:
    if not module_service.is_local(module_name):
        raise HTTPException(404, "Module not found")
    module_service.delete_module(module_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@module_router.delete(
    "/", operation_id="deleteAllModules", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_modules() -> Response:
    for name in module_service.get_local_modules():
        module_service.delete_module(name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@module_router.get("/{module_name}/schema", operation_id="getSchema")
async def get_module_schema(module_name: str) -> SchemaNode:
    if not module_service.is_local(module_name):
        raise HTTPException(404, "Module not downloaded")
    return module_service.get_module_schema(module_name)
