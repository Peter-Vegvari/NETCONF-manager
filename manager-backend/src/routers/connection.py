from fastapi import APIRouter, HTTPException
from src.models.connection import Connection
from src.dependencies import ConnManager

router = APIRouter(tags=["connection"])


@router.post("/connect", operation_id="connect")
async def connect(new_connection: Connection, cm: ConnManager) -> None:
    cm.connection = new_connection
    if cm.connection.connect() is None:
        raise HTTPException(503, "Failed to connect")


@router.delete("/connect", operation_id="disconnect")
async def disconnect_route(cm: ConnManager) -> list[str]:
    cm.connection = None
    return []
