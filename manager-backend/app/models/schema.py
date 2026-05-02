from pydantic import BaseModel


class SchemaNode(BaseModel):
    kind: str = ""
    description: str | None = None
    mandatory: bool | None = None
    default: object | None = None
    type: dict[str, object] | None = None
    children: dict[str, "SchemaNode"] | None = None
