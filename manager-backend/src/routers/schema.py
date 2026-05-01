from fastapi import APIRouter

from src.models.schema import SchemaNode

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("/", operation_id="getSchema")
async def get_schema() -> SchemaNode:
    return SchemaNode.get_schema()
