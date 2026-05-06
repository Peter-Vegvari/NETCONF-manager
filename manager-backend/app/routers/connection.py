from fastapi import APIRouter, HTTPException

import app.dependencies
from app.models.connection import Connection

connection_router = APIRouter(tags=["connection"])


@connection_router.get("/connect", operation_id="getConnectionStatus")
async def get_connection_status() -> bool:
    return app.dependencies.connection_manager.session is not None


@connection_router.post("/connect", operation_id="connect")
async def connect(new_connection: Connection):
    try:
        app.dependencies.connection_manager.connect(new_connection)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@connection_router.delete("/connect", operation_id="disconnect")
async def disconnect_route() -> list[str]:
    app.dependencies.connection_manager.disconnect()
    return []
