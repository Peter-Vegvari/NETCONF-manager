from subprocess import CompletedProcess


from typing import Any, Iterator


from types import ModuleType
from _frozen_importlib import ModuleSpec
from ncclient import manager
from lxml import etree
import subprocess
import importlib.util
import importlib.abc
from pathlib import Path
import os


def download_schemas_yang(host: str, port: int, username: str, password: str):
    with manager.connect(
        host=host,
        port=port,
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


def generate_models():
    yang_dir: Path = Path("resources/modules")
    modules_dir: Path = Path("src/netconf_manager/models")
    failed_modules: list[Path] = []
    modules: Iterator[Path] = yang_dir.glob("*.yang")
    for yang_module in modules:
        result: CompletedProcess[bytes] = subprocess.run(
            [
                "uv",
                "run",
                "pydantify",
                str(yang_module),
                "-i",
                str(yang_dir),
                "-o",
                str(modules_dir),
                "-f",
                f"{yang_module.stem}.py",
            ],
        )
        if result.returncode != 0:
            failed_modules.append(yang_module)
    os.rmdir(modules_dir)

    successful_modules: set[Path] = set[Path](modules) - set[Path](failed_modules)

    subprocess.run(
        [
            "uv",
            "run",
            "pydantify",
            *[str(m) for m in successful_modules],
            "-i",
            str(yang_dir),
            "-o",
            str(modules_dir),
            "-f",
            "models.py",
        ]
    )


def load_generated_model(path: str):
    spec = importlib.util.spec_from_file_location("yang_model", path)
    if spec is None or not isinstance(spec.loader, importlib.abc.Loader):
        raise RuntimeError(f"Could not load module spec from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    generate_models()


if __name__ == "__main__":
    main()
