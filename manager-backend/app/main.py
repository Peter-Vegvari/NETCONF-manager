import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import wireup
import wireup.integration.fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.dependencies as _dependencies
from app.dependencies import ConnectionManager, DownloadedModulesPath
from app.routers.connection import connection_router
from app.routers.modules import module_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(
        "w", dir="/shared", suffix=".tmp", delete=False
    ) as f:
        json.dump(_app.openapi(), f)
        tmp = f.name
    os.replace(tmp, "/shared/openapi.json")
    _dependencies.downloaded_modules_path = await container.get(DownloadedModulesPath)
    _dependencies.connection_manager = await container.get(ConnectionManager)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(module_router)
app.include_router(connection_router)

container = wireup.create_async_container(injectables=[_dependencies])
wireup.integration.fastapi.setup(container, app)
