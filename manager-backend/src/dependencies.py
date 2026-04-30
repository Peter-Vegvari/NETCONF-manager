from pathlib import Path
from typing import final

from wireup import injectable

from src.models.connection import Connection


@injectable
@final
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None


@injectable
@final
class DownloadedModulesPath:
    def __init__(self):
        self.path = Path("../resources/downloaded-modules")
        self.path.mkdir(parents=True, exist_ok=True)


@injectable
@final
class GeneratedModulesPath:
    def __init__(self):
        self.path = Path("../resources/generated-modules")
        self.path.mkdir(parents=True, exist_ok=True)


downloaded_modules_path: DownloadedModulesPath
generated_modules_path: DownloadedModulesPath
connection_manager: ConnectionManager
