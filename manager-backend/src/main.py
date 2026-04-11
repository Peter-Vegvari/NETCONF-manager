import os
from pathlib import Path
import shutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.models import Connection, disconnect
from src.restconf import router as restconf_router

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

app.include_router(restconf_router)

yang_modules: Path = Path("../resources/yang-modules")


@app.post("/connect", operation_id="connect")
async def connect(new_connection: Connection) -> list[str]:
    return new_connection.download_schemas()


@app.delete("/connect", operation_id="disconnect")
async def disconnect_route() -> list[str]:
    deleted_schemas: list[str] = os.listdir(yang_modules) if yang_modules.exists() else []
    disconnect()
    if yang_modules.exists():
        shutil.rmtree(yang_modules)
        os.makedirs(yang_modules)
    return deleted_schemas


@app.get("/schemas", operation_id="getSchemas")
async def get_schemas() -> list[str]:
    if not yang_modules.exists():
        return []
    return os.listdir(yang_modules)


@app.get("/schemas/{schema_name}", operation_id="getSchema", response_model=None)
async def get_schema(schema_name: str) -> FileResponse:
    return FileResponse(f"{yang_modules}/{schema_name}.yang")
