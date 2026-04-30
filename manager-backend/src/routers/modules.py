from fastapi import APIRouter, HTTPException
from wireup import Injected

from src.dependencies import ConnectionManager
from src.models.module import Module

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", operation_id="getModules")
async def get_modules() -> list[Module]:
    generated = Module.get_generated_modules()
    downloaded = Module.get_local_modules()
    remote = Module.get_remote_modules()
    seen = set()
    result = []
    for name in [*generated, *downloaded, *remote]:
        if name not in seen:
            seen.add(name)
            result.append(Module(name=name))
    return result


@router.post("/{module_name}/download", operation_id="downloadModule")
async def download_module(module_name: str):
    Module(name=module_name).download()


@router.delete("/{module_name}", operation_id="deleteModule")
async def delete_module(module_name: str):
    module = Module(name=module_name)
    if not module.exists:
        raise HTTPException(404, "Module not found")
    module.delete()


@router.post("/{module_name}/generate", operation_id="generateModule")
async def generate_module(module_name: str):
    module = Module(name=module_name)
    module.generate()
