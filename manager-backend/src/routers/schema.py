from fastapi import APIRouter

from src.models.schema import SchemaNode

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("/", operation_id="getSchema")
async def get_schema() -> SchemaNode:
    try:
        return SchemaNode.get_schema()
    except Exception:
        return SchemaNode()
