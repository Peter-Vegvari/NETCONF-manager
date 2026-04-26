import os
from pathlib import Path
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.connection import Connection

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(restconf_router)

yang_modules: Path = Path("../resources/yang-modules")
connection: Connection | None = None


@app.post("/connect", operation_id="connect")
async def connect(new_connection: Connection) -> None:
    global connection
    connection = new_connection
    if connection.connect() is None:
        raise HTTPException(503, "Failed to connect")


@app.delete("/connect", operation_id="disconnect")
async def disconnect_route() -> list[str]:
    global connection
    connection = None
    deleted_schemas: list[str] = (
        os.listdir(yang_modules) if yang_modules.exists() else []
    )
    if yang_modules.exists():
        shutil.rmtree(yang_modules)
        os.makedirs(yang_modules)
    return deleted_schemas


@app.get("/modules/available", operation_id="getAvailableModules")
async def get_available_modules() -> list[str]:
    if connection is None:
        raise HTTPException(400, "Not connected")
    modules = connection.get_modules()
    if modules is None:
        raise HTTPException(503, "Failed to connect")
    return modules


@app.get("/modules/", operation_id="getModules")
async def get_modules() -> list[str]:
    if not yang_modules.exists():
        return []
    return os.listdir(yang_modules)


@app.post(
    "/modules/{module_name}/download",
    operation_id="downloadModule"
)
async def download_module(module_name: str):
    result = connection.download_module(module_name)
    if result is None:
        raise HTTPException(503, "Failed to connect")

@app.delete("/modules/{module_name}", operation_id="deleteModule")
async def delete_module(module_name: str):
    os.remove(yang_modules / f"{module_name}.yang")