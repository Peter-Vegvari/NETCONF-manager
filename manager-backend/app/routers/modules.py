import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException

import app.dependencies
from app.models.module import Module, ModuleSummary
from app.models.schema import SchemaNode

module_router = APIRouter(prefix="/modules", tags=["modules"])


@module_router.get("/", operation_id="getModules")
async def get_modules() -> list[ModuleSummary]:
    downloaded = Module.get_local_modules()
    remote = await asyncio.to_thread(Module.get_remote_modules)
    seen: set[str] = set()
    result: list[ModuleSummary] = []
    for mod in [*downloaded, *remote]:
        if mod.name not in seen:
            seen.add(mod.name)
            result.append(mod.to_summary())
    return result


@module_router.post("/download-all", operation_id="downloadAllModules")
async def download_all_modules():
    if app.dependencies.connection_manager.session is None:
        raise HTTPException(400, "Not connected")
    Module.download_all()


@module_router.post("/{module_name}/download", operation_id="downloadModule")
async def download_module(module_name: str):
    Module(name=module_name).download()


@module_router.delete("/{module_name}", operation_id="deleteModule")
async def delete_module(module_name: str):
    module = Module(name=module_name)
    if not module.path.exists():
        raise HTTPException(404, "Module not found")
    module.delete()


@module_router.delete("/", operation_id="deleteAllModules")
async def delete_all_modules():
    for module in Module.get_local_modules():
        module.delete()


@module_router.get("/{module_name}/schema", operation_id="getSchema")
async def get_module_schema(module_name: str) -> SchemaNode:
    module = Module(name=module_name)
    if not module.path.exists():
        raise HTTPException(404, "Module not downloaded")
    return module.schema_node


@module_router.get("/{module_name}/data", operation_id="getModuleData")
async def get_module_data(module_name: str) -> dict[str, Any]:
    if app.dependencies.connection_manager.session is None:
        raise HTTPException(400, "Not connected")
    module = Module(name=module_name)
    schema = module.schema_node
    if not schema.children:
        raise HTTPException(404, "No schema available")
    first_key = next(iter(schema.children))
    top_container = first_key.split(":")[1] if ":" in first_key else first_key
    return module.get_data(top_container)


@module_router.get("/{module_name}/data/{path:path}", operation_id="getData")
async def get_data(module_name: str, path: str) -> dict[str, Any]:
    if app.dependencies.connection_manager.session is None:
        raise HTTPException(400, "Not connected")
    return Module(name=module_name).get_data(path)
