import json
import os
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, cast

from lxml import etree
from lxml.etree import Element
from pydantic import BaseModel
from yangson import DataModel

import app.dependencies
from app.core.config import settings
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


class ModuleSummary(BaseModel):
    name: str
    status: ModuleStatus
    revision: str = ""


class Module(BaseModel):
    name: str

    @property
    def path(self) -> Path:
        return settings.DOWNLOADED_MODULES_PATH / f"{self.name}.yang"

    @property
    def status(self) -> ModuleStatus:
        if self.path.exists():
            return ModuleStatus.LOCAL
        return ModuleStatus.REMOTE

    def to_summary(self) -> "ModuleSummary":
        return ModuleSummary(name=self.name, status=self.status, revision=self.revision)

    def download(self) -> None:
        m = app.dependencies.connection_manager.session
        assert m is not None
        content = cast(str, cast(Any, m).get_schema(identifier=self.name).data)
        with open(self.path, "w", encoding="utf-8") as f:
            _ = f.write(content)

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

    @property
    def namespace(self) -> str:
        if not self.path.exists():
            return ""
        with open(self.path, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("namespace "):
                    return stripped.split('"')[1] if '"' in stripped else ""
        return ""

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

    def get_data(self, path: str) -> dict[str, Any]:
        s = app.dependencies.connection_manager.session
        assert s is not None
        parts = path.strip("/").split("/")
        root = parts[0]
        inner = "".join(f"<{p}/>" for p in parts[1:]) if len(parts) > 1 else ""
        ns = self.namespace or f"urn:ietf:params:xml:ns:yang:{self.name}"
        subtree = f'<{root} xmlns="{ns}">{inner}</{root}>'
        reply = cast(Any, s).get(filter=("subtree", subtree))
        return Module._xml_to_json(cast(Element, reply.data_ele), self.name)

    @staticmethod
    def _xml_to_json(data_ele: Element, module_name: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for child in data_ele:
            tag = etree.QName(child).localname
            key = f"{module_name}:{tag}"
            value = Module._element_to_value(child)
            if key in result:
                existing = result[key]
                if isinstance(existing, list):
                    cast(list[Any], existing).append(value)
                else:
                    result[key] = [existing, value]
            else:
                result[key] = value
        return result

    @staticmethod
    def _element_to_value(el: Element) -> Any:
        children = list(el)
        if not children:
            return el.text or ""
        result: dict[str, Any] = {}
        for child in children:
            tag = etree.QName(child).localname
            value = Module._element_to_value(child)
            if tag in result:
                existing = result[tag]
                if isinstance(existing, list):
                    cast(list[Any], existing).append(value)
                else:
                    result[tag] = [existing, value]
            else:
                result[tag] = value
        return result

    def delete(self) -> None:
        self.path.unlink(missing_ok=True)

    @staticmethod
    def download_all() -> None:
        m = app.dependencies.connection_manager.session
        assert m is not None
        for module in Module.get_remote_modules():
            if module.path.exists():
                continue
            try:
                content = cast(
                    str, cast(Any, m).get_schema(identifier=module.name).data
                )
                with open(module.path, "w", encoding="utf-8") as f:
                    _ = f.write(content)
            except Exception:
                pass

    @staticmethod
    def get_remote_modules() -> "list[Module]":
        m = app.dependencies.connection_manager.session
        if m is None:
            return []
        try:
            reply = cast(Any, m).get(filter=("subtree", _NETCONF_SCHEMAS_FILTER))
            xml = cast(str, reply.xml)
            tree = etree.fromstring(xml.encode("utf-8"))
            schemas = tree.xpath("//ncm:schema", namespaces=_NETCONF_NS)
            return [
                Module(
                    name=s.findtext(
                        "ncm:identifier", default="", namespaces=_NETCONF_NS
                    )
                )
                for s in schemas
            ]
        except Exception:
            return []

    @staticmethod
    def get_local_modules() -> "list[Module]":
        return [
            Module(name=f.removesuffix(".yang"))
            for f in os.listdir(settings.DOWNLOADED_MODULES_PATH)
            if f.endswith(".yang")
        ]

    @staticmethod
    def _build_data_model() -> DataModel:
        modules = Module.get_local_modules()
        yang_library = {
            "ietf-yang-library:modules-state": {
                "module-set-id": "1",
                "module": [
                    {
                        "name": m.name,
                        "revision": m.revision,
                        "namespace": m.namespace,
                        "conformance-type": "implement",
                    }
                    for m in modules
                ],
            }
        }
        modules_path = settings.DOWNLOADED_MODULES_PATH
        return DataModel(json.dumps(yang_library), mod_path=[str(modules_path)])

    @staticmethod
    def get_schemas() -> "SchemaNode":
        dm = Module._build_data_model()
        return SchemaNode.model_validate(json.loads(dm.schema_digest()))
