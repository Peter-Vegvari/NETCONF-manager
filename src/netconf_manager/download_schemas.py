from subprocess import CompletedProcess


from typing import Any, Iterator
from types import CoroutineType, ModuleType
from _frozen_importlib import ModuleSpec
from ncclient import manager
from lxml import etree
import subprocess
import importlib.util
import importlib.abc
from pathlib import Path
import tempfile
import asyncio


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


async def run_pydantify(
    yang_module: Path, yang_dir: Path, modules_dir: Path
) -> tuple[Path, int]:
    with tempfile.TemporaryDirectory() as tmp:
        proc = await asyncio.create_subprocess_exec(
            "uv",
            "run",
            "pydantify",
            str(yang_module),
            "-i",
            str(yang_dir),
            "-o",
            tmp,
            "-f",
            "_.py",
            stderr=asyncio.subprocess.DEVNULL,
        )
        returncode = await proc.wait()
    return yang_module, returncode


async def generate_models():
    yang_dir: Path = Path("resources/modules")
    modules_dir: Path = Path("src/netconf_manager/models")
    modules: Iterator[Path] = yang_dir.glob("*.yang")

    tasks: list[CoroutineType[Any, Any, tuple[Path, int]]] = [
        run_pydantify(m, yang_dir, modules_dir) for m in modules
    ]

    results: list[tuple[Path, int]] = await asyncio.gather(*tasks)
    successful_modules: list[Path] = [path for path, code in results if code == 0]

    print(results)
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
    asyncio.run(generate_models())


if __name__ == "__main__":
    main()
