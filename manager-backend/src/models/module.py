import os
import subprocess
from enum import StrEnum, auto
from pathlib import Path

from lxml import etree
from pydantic import BaseModel, computed_field

import src.dependencies


class ModuleStatus(StrEnum):
    REMOTE = auto()
    LOCAL = auto()
    GENERATED = auto()


class Module(BaseModel):
    name: str

    @computed_field
    @property
    def status(self) -> ModuleStatus:
        if self.generated_model_path.exists():
            return ModuleStatus.GENERATED
        if self.yang_module_path.exists():
            return ModuleStatus.LOCAL
        return ModuleStatus.REMOTE

    @computed_field
    @property
    def yang_module_path(self) -> Path:
        return src.dependencies.downloaded_modules_path.path / f"{self.name}.yang"

    @computed_field
    @property
    def generated_model_path(self) -> Path:
        return src.dependencies.GeneratedModulesPath().path / f"{self.name}.py"

    @computed_field
    @property
    def exists(self) -> bool:
        return self.yang_module_path.exists()

    def download(self) -> None:
        connection = src.dependencies.connection_manager.connection
        assert connection is not None
        with connection.connect() as m:
            with open(self.yang_module_path, "w", encoding="utf-8") as f:
                f.write(m.get_schema(identifier=self.name).data)

    def delete(self) -> None:
        self.yang_module_path.unlink(missing_ok=True)
        self.generated_model_path.unlink(missing_ok=True)

    def generate(self) -> None:
        _ = subprocess.run(
            [
                "uv",
                "run",
                "pydantify",
                "-i",
                str(src.dependencies.downloaded_modules_path.path),
                "-o",
                str(src.dependencies.generated_modules_path.path),
                "-f",
                f"{self.name}.py",
                str(self.yang_module_path),
            ]
        )

    @staticmethod
    def get_remote_modules() -> list[str]:
        connection = src.dependencies.connection_manager.connection
        if connection is None:
            return []
        with connection.connect() as m:
            filter_xml = """
                    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
                        <schemas/>
                    </netconf-state>
                """
            reply = m.get(filter=("subtree", filter_xml))
            tree = etree.fromstring(reply.xml.encode())
            ns = {"ncm": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"}
            schemas = tree.xpath("//ncm:schema", namespaces=ns)
            return [s.find("ncm:identifier", ns).text for s in schemas]

    @staticmethod
    def get_local_modules() -> list[str]:
        modules = src.dependencies.downloaded_modules_path.path
        if not modules.exists():
            return []
        return [f.removesuffix(".yang") for f in os.listdir(modules)]

    @staticmethod
    def get_generated_modules() -> list[str]:
        modules = src.dependencies.generated_modules_path.path
        if not modules.exists():
            return []
        return [f.removesuffix(".py") for f in os.listdir(modules)]
