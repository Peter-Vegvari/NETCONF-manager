import os
from pathlib import Path
from lxml import etree
from pydantic import BaseModel
from src.models.connection import Connection


class Module(BaseModel):
    name: str
    downloadable: bool | None

    def download(self, connection: Connection, yang_modules: Path):
        m = connection.connect()
        if m is None:
            return None
        with m:
            yang_module = Path(yang_modules, f"{self.name}.yang")
            with open(yang_module, "w", encoding="utf-8") as f:
                f.write(m.get_schema(identifier=self.name).data)

    @staticmethod
    def get_remote_modules(connection: Connection) -> list[str]:
        m = connection.connect()
        if m is None:
            return []
        with m:
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
    def get_local_modules(yang_modules: Path) -> list[str]:
        if not yang_modules.exists():
            return []
        return [f.removesuffix(".yang") for f in os.listdir(yang_modules)]
