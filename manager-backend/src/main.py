import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import wireup
import wireup.integration.fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.dependencies
from src.routers.connection import router as connection_router
from src.routers.modules import router as modules_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    with open("/shared/openapi.json", "w") as f:
        json.dump(app.openapi(), f)
    src.dependencies.downloaded_modules_path = await container.get(
        src.dependencies.DownloadedModulesPath
    )
    src.dependencies.generated_modules_path = await container.get(
        src.dependencies.GeneratedModulesPath
    )
    src.dependencies.connection_manager = await container.get(
        src.dependencies.ConnectionManager
    )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(modules_router)
app.include_router(connection_router)

container = wireup.create_async_container(injectables=[src.dependencies])
wireup.integration.fastapi.setup(container, app)
