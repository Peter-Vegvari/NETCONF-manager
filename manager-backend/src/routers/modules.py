from fastapi import APIRouter, HTTPException
from wireup import Injected

from src.dependencies import ConnectionManager
from src.models.module import Module

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", operation_id="getModules")
async def get_modules(cm: Injected[ConnectionManager]) -> list[Module]:
    if cm.connection is None:
        raise HTTPException(503, "Failed to connect")

    available = Module.get_remote_modules()
    downloaded = Module.get_local_modules()
    return [Module(name=m, downloadable=m not in downloaded) for m in available]


@router.post("/{module_name}/download", operation_id="downloadModule")
async def download_module(module_name: str, cm: Injected[ConnectionManager]):
    if cm.connection is None:
        raise HTTPException(400, "Not connected")
    Module(name=module_name, downloadable=None).download()


@router.delete("/{module_name}", operation_id="deleteModule")
async def delete_module(module_name: str):
    module = Module(name=module_name)
    if not module.exists:
        raise HTTPException(404, "Module not found")
    module.delete()
