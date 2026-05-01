import json

from pydantic import BaseModel, Field
from yangson import DataModel

import src.dependencies
from src.models.module import Module


class YangModuleEntry(BaseModel):
    name: str
    revision: str
    conformance_type: str = Field(
        default="implement", serialization_alias="conformance-type"
    )


class YangLibrary(BaseModel):
    module_set_id: str = Field(default="1", serialization_alias="module-set-id")
    module: list[YangModuleEntry] = []


class SchemaNode(BaseModel):
    kind: str = ""
    description: str | None = None
    mandatory: bool | None = None
    default: object | None = None
    type: dict[str, object] | None = None
    children: dict[str, "SchemaNode"] | None = None


def _parse_revision(path: object) -> str:
    """Extract the first revision string from a YANG file."""
    with open(str(path), "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("revision "):
                return stripped.split()[1].rstrip("{").strip('"').strip("'")
    return ""


def get_schema() -> SchemaNode:
    """Build a SchemaNode tree from all locally downloaded YANG modules."""
    entries = [
        YangModuleEntry(name=m.name, revision=_parse_revision(m.yang_module_path))
        for m in Module.get_local_modules()
    ]

    yang_library = {
        "ietf-yang-library:modules-state": YangLibrary(module=entries).model_dump(
            by_alias=True
        ),
    }

    modules_path = src.dependencies.downloaded_modules_path.path
    dm = DataModel(json.dumps(yang_library), mod_path=[str(modules_path)])
    return SchemaNode.model_validate(json.loads(dm.schema_digest()))
