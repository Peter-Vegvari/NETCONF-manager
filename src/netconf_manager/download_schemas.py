from ncclient import manager
import json
from lxml import etree
import requests
from yangson import DataModel


def download_schemas_yang(host: str, username: str, password: str):
    with manager.connect(
        host=host,
        port=830,
        username=username,
        password=password,
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


def download_schemas_json():
    # url = "http://localhost:8000/restconf/data/ietf-yang-library:modules-state"

    # r = requests.get(url).json()
    dm = DataModel.from_file("yang-library.json", ["resources/modules"])
    schema = dm.get_schema_node("/ietf-interfaces:interfaces/interface")
    print(schema)
    
def main():
    download_schemas_json()

if __name__ == "__main__":
    main()
