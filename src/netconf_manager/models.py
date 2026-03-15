from pydantic import BaseModel
from ncclient import manager
from lxml import etree


class Connection(BaseModel):
    host: str = "localhost"
    port: int = 830
    user_name: str = "admin"
    password: str = "admin"

    def download_schemas(self):
        with manager.connect(
            host=self.host,
            port=self.port,
            username=self.user_name,
            password=self.password,
            hostkey_verify=False,
            device_params={"name": "default"},
            allow_agent=False,
            look_for_keys=False,
        ) as m:
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

            print(f"Downloading {identifier}")

            schema_reply = m.get_schema(identifier=identifier)

            filename = f"{identifier}.yang"
            with open("resources/modules/" + filename, "w", encoding="utf-8") as f:
                f.write(schema_reply.data)
