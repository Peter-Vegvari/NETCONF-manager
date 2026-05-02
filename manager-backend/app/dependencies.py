from pathlib import Path
from typing import final

from wireup import injectable

from app.models.connection import Connection


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


downloaded_modules_path: DownloadedModulesPath
connection_manager: ConnectionManager
