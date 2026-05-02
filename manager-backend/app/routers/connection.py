from fastapi import APIRouter, HTTPException
from wireup import Injected

from app.dependencies import ConnectionManager
from app.models.connection import Connection

connection_router = APIRouter(tags=["connection"])


@connection_router.post("/connect", operation_id="connect")
async def connect(new_connection: Connection, cm: Injected[ConnectionManager]) -> None:
    try:
        new_connection.connect()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    cm.connection = new_connection


@connection_router.delete("/connect", operation_id="disconnect")
async def disconnect_route(cm: Injected[ConnectionManager]) -> list[str]:
    cm.connection = None
    return []
