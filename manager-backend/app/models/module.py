import json
import os
from enum import StrEnum, auto
from pathlib import Path

from lxml import etree
from pydantic import BaseModel, computed_field
from yangson import DataModel

import app.dependencies
from app.models.schema import SchemaNode

_NETCONF_SCHEMAS_FILTER = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <schemas/>
    </netconf-state>
"""
_NETCONF_NS = {"ncm": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"}


class ModuleStatus(StrEnum):
    REMOTE = auto()
    LOCAL = auto()


class Module(BaseModel):
    name: str

    @computed_field
    @property
    def path(self) -> Path:
        return app.dependencies.downloaded_modules_path.path / f"{self.name}.yang"

    @computed_field
    @property
    def status(self) -> ModuleStatus:
        if self.path.exists():
            return ModuleStatus.LOCAL
        return ModuleStatus.REMOTE

    def download(self) -> None:
        connection = app.dependencies.connection_manager.connection
        assert connection is not None
        with connection.connect() as m:
            content = m.get_schema(identifier=self.name).data
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(content)

    @computed_field
    @property
    def revision(self) -> str:
        if not self.path.exists():
            return ""
        with open(self.path, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("revision "):
                    return stripped.split()[1].rstrip("{").strip('"').strip("'")
        return ""

    @computed_field
    @property
    def schema_node(self) -> SchemaNode:
        try:
            full = Module.get_schemas()
        except Exception:
            return SchemaNode()
        if not full.children:
            return SchemaNode()
        filtered = {
            k: v for k, v in full.children.items() if k.startswith(f"{self.name}:")
        }
        return SchemaNode(children=filtered if filtered else None)

    def delete(self) -> None:
        self.path.unlink(missing_ok=True)

    @staticmethod
    def download_all() -> None:
        connection = app.dependencies.connection_manager.connection
        assert connection is not None
        with connection.connect() as m:
            for module in Module.get_remote_modules():
                if module.path.exists():
                    continue
                try:
                    content = m.get_schema(identifier=module.name).data
                    with open(module.path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception:
                    pass

    @staticmethod
    def get_remote_modules() -> "list[Module]":
        if app.dependencies.connection_manager.connection is None:
            return []
        with app.dependencies.connection_manager.connection.connect() as m:
            reply = m.get(filter=("subtree", _NETCONF_SCHEMAS_FILTER))
            tree = etree.fromstring(reply.xml.encode())
            schemas = tree.xpath("//ncm:schema", namespaces=_NETCONF_NS)
            return [
                Module(name=s.find("ncm:identifier", _NETCONF_NS).text) for s in schemas
            ]

    @staticmethod
    def get_local_modules() -> "list[Module]":
        return [
            Module(name=f.removesuffix(".yang"))
            for f in os.listdir(app.dependencies.downloaded_modules_path.path)
            if f.endswith(".yang")
        ]

    @staticmethod
    def get_schemas() -> "SchemaNode":
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

        modules_path = app.dependencies.downloaded_modules_path.path
        dm = DataModel(json.dumps(yang_library), mod_path=[str(modules_path)])
        return SchemaNode.model_validate(json.loads(dm.schema_digest()))
