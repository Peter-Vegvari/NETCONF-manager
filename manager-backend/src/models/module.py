import os
import subprocess

from lxml import etree
from pydantic import BaseModel, computed_field

import src.dependencies


class Module(BaseModel):
    name: str
    downloadable: bool | None = None

    @computed_field
    @property
    def get_yang_module_name(self) -> str:
        return f"{self.name}.yang"

    @computed_field
    @property
    def get_generated_model_name(self) -> str:
        return f"{self.name}.py"

    @computed_field
    @property
    def exists(self) -> bool:
        return (
            src.dependencies.yang_modules_path.path / self.get_yang_module_name
        ).exists()

    def download(self) -> None:
        connection = src.dependencies.connection_manager.connection
        assert connection is not None
        with connection.connect() as m:
            yang_module = (
                src.dependencies.yang_modules_path.path / self.get_yang_module_name
            )
            with open(yang_module, "w", encoding="utf-8") as f:
                f.write(m.get_schema(identifier=self.name).data)

    def delete(self) -> None:
        (src.dependencies.yang_modules_path.path / self.get_yang_module_name).unlink(
            missing_ok=True
        )

    def generate(self) -> None:
        _ = subprocess.run(
            [
                "uv",
                "run",
                "pydantify",
                "-i",
                str(src.dependencies.yang_modules_path.path),
                "-o",
                str(src.dependencies.yang_modules_path.path),
                "-f",
                f"{self.name}.py",
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
            print(reply)
            tree = etree.fromstring(reply.xml.encode())
            ns = {"ncm": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"}
            schemas = tree.xpath("//ncm:schema", namespaces=ns)
            return [s.find("ncm:identifier", ns).text for s in schemas]

    @staticmethod
    def get_local_modules() -> list[str]:
        yang_modules = src.dependencies.yang_modules_path.path
        if not yang_modules.exists():
            return []
        return [f.removesuffix(".yang") for f in os.listdir(yang_modules)]
