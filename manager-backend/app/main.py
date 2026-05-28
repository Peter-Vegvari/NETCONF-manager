import json
import os
import tempfile
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import wireup
import wireup.integration.fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.services.connection_service as _connection_service
from app.core.config import settings
from app.routers.connection_router import connection_router
from app.routers.datastore_router import datastore_router
from app.routers.module_router import module_router
from app.services.connection_service import ConnectionManager


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    settings.DOWNLOADED_MODULES_PATH.mkdir(parents=True, exist_ok=True)

    if settings.ENVIRONMENT != "testing":
        with tempfile.NamedTemporaryFile(
            "w", dir="/shared", suffix=".tmp", delete=False
        ) as f:
            json.dump(_app.openapi(), f)
            tmp = f.name
        os.replace(tmp, "/shared/openapi.json")
    _connection_service.connection_manager = await container.get(ConnectionManager)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(module_router, prefix=settings.API_V1_STR)
app.include_router(connection_router, prefix=settings.API_V1_STR)
app.include_router(datastore_router, prefix=settings.API_V1_STR)

container = wireup.create_async_container(injectables=[_connection_service])
wireup.integration.fastapi.setup(container, app)
