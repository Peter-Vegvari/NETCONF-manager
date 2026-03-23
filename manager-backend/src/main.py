from starlette.responses import FileResponse


import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.models import Connection, Schema

# uv run fastapi dev manager_backend/main.py
app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection: Connection | None = None
yang_modules: Path = Path("../resources/yang-modules")


@app.post("/connect")
async def connect(new_connection: Connection) -> list[str]:
    global connection
    connection = new_connection
    return connection.download_schemas()


@app.delete("/connect")
async def disconnect() -> list[str]:
    deleted_schemas: list[str] = os.listdir(yang_modules)

    shutil.rmtree(yang_modules)
    os.makedirs(yang_modules)

    return deleted_schemas


@app.post("/netconf/get")
async def get():
    pass


@app.post("/netconf/get-config")
async def get_config():
    pass


@app.get("/netconf/get-schemas")
async def get_schemas() -> list[str]:
    return os.listdir(yang_modules)


@app.get("/netconf/get-schema/{schema_name}", response_model=None)
async def get_schema(schema_name: str ) -> FileResponse:
    return FileResponse(f"{yang_modules}/{schema_name}.yang")


@app.post("/netconf/dispatch")
async def dispatch():
    pass


@app.post("/netconf/edit-config")
async def edit_config():
    pass


@app.post("/netconf/copy-config")
async def copy_config():
    pass


@app.post("/netconf/validate")
async def validate():
    pass


@app.post("/netconf/commit")
async def commit():
    pass


@app.post("/netconf/discard-changes")
async def discard_changes():
    pass


@app.post("/netconf/cancel-commit")
async def cancel_commit():
    pass


@app.post("/netconf/delete-config")
async def delete_config():
    pass


@app.post("/netconf/lock")
async def lock():
    pass


@app.post("/netconf/unlock")
async def unlock():
    pass


@app.post("/netconf/create-subscription")
async def create_subscription():
    pass


@app.post("/netconf/close-session")
async def close_session():
    pass


@app.post("/netconf/kill-session")
async def kill_session():
    pass


@app.post("/netconf/poweroff-machine")
async def poweroff_machine():
    pass


@app.post("/netconf/reboot-machine")
async def reboot_machine():
    pass


@app.post("/netconf/rpc")
async def rpc():
    pass
