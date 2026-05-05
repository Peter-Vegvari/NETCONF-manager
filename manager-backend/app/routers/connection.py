from fastapi import APIRouter

import app.dependencies
from app.models.connection import Connection

connection_router = APIRouter(tags=["connection"])


@connection_router.post("/connect", operation_id="connect")
async def connect(new_connection: Connection):
    app.dependencies.connection_manager.connection = new_connection


@connection_router.delete("/connect", operation_id="disconnect")
async def disconnect_route() -> list[str]:
    app.dependencies.connection_manager.connection = None
    return []
