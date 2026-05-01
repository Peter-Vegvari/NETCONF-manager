import json

from pydantic import BaseModel
from yangson import DataModel

import src.dependencies
from src.models.module import Module


class SchemaNode(BaseModel):
    kind: str = ""
    description: str | None = None
    mandatory: bool | None = None
    default: object | None = None
    type: dict[str, object] | None = None
    children: dict[str, "SchemaNode"] | None = None

    @staticmethod
    def get_schema() -> SchemaNode:
        modules = Module.get_local_modules()

        yang_library = {
            "ietf-yang-library:modules-state": {
                "module-set-id": "1",
                "module": [
                    {
                        "name": m.name,
                        "revision": m.revision,
                        "conformance-type": "implement",
                    }
                    for m in modules
                ],
            }
        }

        modules_path = src.dependencies.downloaded_modules_path.path
        dm = DataModel(json.dumps(yang_library), mod_path=[str(modules_path)])
        return SchemaNode.model_validate(json.loads(dm.schema_digest()))
