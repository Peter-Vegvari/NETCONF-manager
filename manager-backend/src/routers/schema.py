from fastapi import APIRouter

from src.models.module import Module
from src.models.schema import SchemaNode

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("/", operation_id="getSchema")
async def get_schema() -> SchemaNode:
    return Module.get_schema()
