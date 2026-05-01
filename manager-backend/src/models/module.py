import os
from enum import StrEnum, auto
from pathlib import Path

from lxml import etree
from pydantic import BaseModel, computed_field

import src.dependencies

_NETCONF_SCHEMAS_FILTER = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <schemas/>
    </netconf-state>
"""
_NETCONF_NS = {"ncm": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"}


def _fetch_remote_modules(session) -> "list[Module]":
    """Fetch modules from a NETCONF session."""
    reply = session.get(filter=("subtree", _NETCONF_SCHEMAS_FILTER))
    tree = etree.fromstring(reply.xml.encode())
    schemas = tree.xpath("//ncm:schema", namespaces=_NETCONF_NS)
    return [Module(name=s.find("ncm:identifier", _NETCONF_NS).text) for s in schemas]


class ModuleStatus(StrEnum):
    REMOTE = auto()
    LOCAL = auto()


class Module(BaseModel):
    name: str

    @computed_field
    @property
    def yang_module_path(self) -> Path:
        return src.dependencies.downloaded_modules_path.path / f"{self.name}.yang"

    @computed_field
    @property
    def status(self) -> ModuleStatus:
        if self.yang_module_path.exists():
            return ModuleStatus.LOCAL
        return ModuleStatus.REMOTE

    def download(self) -> None:
        connection = src.dependencies.connection_manager.connection
        assert connection is not None
        with connection.connect() as m:
            with open(self.yang_module_path, "w", encoding="utf-8") as f:
                f.write(m.get_schema(identifier=self.name).data)

    def delete(self) -> None:
        self.yang_module_path.unlink(missing_ok=True)

    @staticmethod
    def download_all() -> None:
        assert src.dependencies.connection_manager.connection is not None
        with src.dependencies.connection_manager.connection.connect() as m:
            for mod in _fetch_remote_modules(m):
                if mod.yang_module_path.exists():
                    continue
                try:
                    with open(mod.yang_module_path, "w", encoding="utf-8") as f:
                        f.write(m.get_schema(identifier=mod.name).data)
                except Exception:
                    pass

    @staticmethod
    def get_remote_modules() -> "list[Module]":
        if src.dependencies.connection_manager.connection is None:
            return []
        with src.dependencies.connection_manager.connection.connect() as m:
            return _fetch_remote_modules(m)

    @staticmethod
    def get_local_modules() -> "list[Module]":
        return [
            Module(name=f.removesuffix(".yang"))
            for f in os.listdir(src.dependencies.downloaded_modules_path.path)
            if f.endswith(".yang")
        ]
