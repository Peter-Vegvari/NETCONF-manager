import os
from fastapi import APIRouter, HTTPException
from src.models.module import Module
from src.dependencies import YangModulesPath, ConnManager

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", operation_id="getModules")
async def get_modules(yang_modules: YangModulesPath, cm: ConnManager) -> list[Module]:
    if cm.connection is None:
        raise HTTPException(503, "Failed to connect")

    available = Module.get_remote_modules(cm.connection)
    downloaded = Module.get_local_modules(yang_modules)
    result = [Module(name=m, downloadable= m not in downloaded) for m in available]
    return result


@router.post("/{module_name}/download", operation_id="downloadModule")
async def download_module(
    module_name: str, cm: ConnManager, yang_modules: YangModulesPath
):
    if cm.connection is None:
        raise HTTPException(400, "Not connected")
    module = Module(name=module_name, downloadable=None)
    module.download(cm.connection, yang_modules)


@router.delete("/{module_name}", operation_id="deleteModule")
async def delete_module(module_name: str, yang_modules: YangModulesPath):
    os.remove(yang_modules / f"{module_name}.yang")
