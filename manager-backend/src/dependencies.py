from pathlib import Path

from wireup import injectable

from src.models.connection import Connection


@injectable
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None


@injectable
class YangModulesPath:
    def __init__(self):
        self.path = Path("../resources/yang-modules")


@injectable
class GeneratedModulesPath:
    def __init__(self):
        self.path = Path("models/generated")


yang_modules_path: YangModulesPath
connection_manager: ConnectionManager
