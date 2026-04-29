from fastapi import APIRouter, HTTPException
from wireup import Injected

from src.dependencies import ConnectionManager
from src.models.connection import Connection

router = APIRouter(tags=["connection"])


@router.post("/connect", operation_id="connect")
async def connect(new_connection: Connection, cm: Injected[ConnectionManager]) -> None:
    cm.connection = new_connection
    if cm.connection.connect() is None:
        raise HTTPException(503, "Failed to connect")


@router.delete("/connect", operation_id="disconnect")
async def disconnect_route(cm: Injected[ConnectionManager]) -> list[str]:
    cm.connection = None
    return []
