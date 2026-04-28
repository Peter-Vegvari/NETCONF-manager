import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.modules import router as modules_router
from src.routers.connection import router as connection_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(modules_router)
app.include_router(connection_router)


@app.on_event("startup")
def export_openapi():
    with open("/shared/openapi.json", "w") as f:
        json.dump(app.openapi(), f)
