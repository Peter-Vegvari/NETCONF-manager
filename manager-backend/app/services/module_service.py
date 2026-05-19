import json
import os
from pathlib import Path
from typing import Any, cast

from lxml import etree
from lxml.etree import Element
from pyang.context import Context
from pyang.repository import FileRepository
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


def module_path(name: str) -> Path:
    return settings.DOWNLOADED_MODULES_PATH / f"{name}.yang"


def is_local(name: str) -> bool:
    return module_path(name).exists()


def get_revision(name: str) -> str:
    p = module_path(name)
    if not p.exists():
        return ""
    repo = FileRepository(str(p.parent))
    ctx = cast(Any, Context(repo))
    with open(p, "r") as f:
        module = ctx.add_module(str(p), f.read())
    if module is None:
        return ""
    rev = module.search_one("revision")
    return cast(str, rev.arg) if rev else ""


def get_namespace(name: str) -> str:
    p = module_path(name)
    if not p.exists():
        return ""
    repo = FileRepository(str(p.parent))
    ctx = cast(Any, Context(repo))
    with open(p, "r") as f:
        module = ctx.add_module(str(p), f.read())
    if module is None:
        return ""
    ns = module.search_one("namespace")
    return cast(str, ns.arg) if ns else ""


def get_remote_modules() -> list[str]:
    m = app.dependencies.connection_manager.session
    if m is None:
        return []
    try:
        reply = cast(Any, m).get(filter=("subtree", _NETCONF_SCHEMAS_FILTER))
        xml = cast(str, reply.xml)
        tree = etree.fromstring(xml.encode("utf-8"))
        schemas = tree.xpath("//ncm:schema", namespaces=_NETCONF_NS)
        return [
            s.findtext("ncm:identifier", default="", namespaces=_NETCONF_NS)
            for s in schemas
        ]
    except Exception:
        return []


def get_local_modules() -> list[str]:
    return [
        f.removesuffix(".yang")
        for f in os.listdir(settings.DOWNLOADED_MODULES_PATH)
        if f.endswith(".yang")
    ]


def download_module(name: str) -> None:
    m = app.dependencies.connection_manager.session
    assert m is not None
    content = cast(str, cast(Any, m).get_schema(identifier=name).data)
    with open(module_path(name), "w", encoding="utf-8") as f:
        _ = f.write(content)


def download_all() -> None:
    m = app.dependencies.connection_manager.session
    assert m is not None
    for name in get_remote_modules():
        if module_path(name).exists():
            continue
        try:
            content = cast(str, cast(Any, m).get_schema(identifier=name).data)
            with open(module_path(name), "w", encoding="utf-8") as f:
                _ = f.write(content)
        except Exception:
            pass


def delete_module(name: str) -> None:
    module_path(name).unlink(missing_ok=True)


def get_schemas() -> SchemaNode:
    dm = _build_data_model()
    return SchemaNode.model_validate(json.loads(dm.schema_digest()))


def get_module_schema(name: str) -> SchemaNode:
    try:
        full = get_schemas()
    except Exception:
        return SchemaNode()
    if not full.children:
        return SchemaNode()
    filtered = {k: v for k, v in full.children.items() if k.startswith(f"{name}:")}
    return SchemaNode(children=filtered if filtered else None)


def get_data(module_name: str, data_store: Any, path: str) -> dict[str, Any]:
    s = app.dependencies.connection_manager.session
    assert s is not None
    parts = path.strip("/").split("/")
    root = parts[0]
    inner = "".join(f"<{p}/>" for p in parts[1:]) if len(parts) > 1 else ""
    ns = get_namespace(module_name) or f"urn:ietf:params:xml:ns:yang:{module_name}"
    subtree = f'<{root} xmlns="{ns}">{inner}</{root}>'
    reply = cast(Any, s).get_config(data_store, filter=("subtree", subtree))
    return _xml_to_json(cast(Element, reply.data_ele), module_name)


# --- private helpers ---


def _build_data_model() -> DataModel:
    modules = get_local_modules()
    yang_library = {
        "ietf-yang-library:modules-state": {
            "module-set-id": "1",
            "module": [
                {
                    "name": name,
                    "revision": get_revision(name),
                    "namespace": get_namespace(name),
                    "conformance-type": "implement",
                }
                for name in modules
            ],
        }
    }
    return DataModel(
        json.dumps(yang_library), mod_path=[str(settings.DOWNLOADED_MODULES_PATH)]
    )


def _xml_to_json(data_ele: Element, module_name: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for child in data_ele:
        tag = etree.QName(child).localname
        key = f"{module_name}:{tag}"
        value = _element_to_value(child)
        if key in result:
            existing = result[key]
            if isinstance(existing, list):
                cast(list[Any], existing).append(value)
            else:
                result[key] = [existing, value]
        else:
            result[key] = value
    return result


def _element_to_value(el: Element) -> Any:
    children = list(el)
    if not children:
        return el.text or ""
    result: dict[str, Any] = {}
    for child in children:
        tag = etree.QName(child).localname
        value = _element_to_value(child)
        if tag in result:
            existing = result[tag]
            if isinstance(existing, list):
                cast(list[Any], existing).append(value)
            else:
                result[tag] = [existing, value]
        else:
            result[tag] = value
    return result
