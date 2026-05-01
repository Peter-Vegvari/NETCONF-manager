from typing import Any

from pydantic import BaseModel


class SchemaNode(BaseModel):
    kind: str = ""
    description: str | None = None
    mandatory: bool | None = None
    default: Any | None = None
    type: dict[str, Any] | None = None
    children: dict[str, "SchemaNode"] | None = None
