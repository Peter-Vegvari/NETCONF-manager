from fastapi import APIRouter, HTTPException, Response, status

import app.services.connection_service
from app.models import Connection

connection_router = APIRouter(tags=["connection"])


@connection_router.get("/connect", operation_id="getConnectionStatus")
async def get_connection_status() -> bool:
    return app.services.connection_service.connection_manager.is_connected


@connection_router.post(
    "/connect", operation_id="connect", status_code=status.HTTP_204_NO_CONTENT
)
async def connect(new_connection: Connection) -> Response:
    try:
        app.services.connection_service.connection_manager.connect(new_connection)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@connection_router.delete("/connect", operation_id="disconnect")
async def disconnect_route() -> list[str]:
    app.services.connection_service.connection_manager.disconnect()
    return []
