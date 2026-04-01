from pydantic import BaseModel
from ncclient import manager
import os
from lxml import etree
from pathlib import Path


class Connection(BaseModel):
    host: str = "notconf"
    port: int = 830
    user_name: str = "admin"
    password: str = "admin"
    yang_modules: Path = Path("../resources/yang-modules")

    def download_schemas(self) -> list[str]:
        downloaded: list[str] = []
        connection = manager.connect(
            host=self.host,
            port=self.port,
            username=self.user_name,
            password=self.password,
            hostkey_verify=False,
            device_params={"name": "default"},
            allow_agent=False,
            look_for_keys=False,
        )

        if connection is None:
            return downloaded

        os.makedirs(self.yang_modules, exist_ok=True)
        with connection as m:
            filter_xml = """
                <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
                    <schemas/>
                </netconf-state>
            """

            reply = m.get(filter=("subtree", filter_xml))

            tree = etree.fromstring(reply.xml.encode())

            ns = {"ncm": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"}

            schemas = tree.xpath("//ncm:schema", namespaces=ns)

            for schema in schemas:
                identifier = schema.find("ncm:identifier", ns).text
                yang_module = Path(self.yang_modules, f"{identifier}.yang")

                if not os.path.exists(yang_module):
                    print(f"Downloading {identifier}")
                    with open(yang_module, "w", encoding="utf-8") as f:
                        f.write(m.get_schema(identifier=identifier).data)
                    downloaded.append(identifier)
            return downloaded


class Schema(BaseModel):
    name: str
