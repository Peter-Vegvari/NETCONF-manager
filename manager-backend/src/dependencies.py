from pathlib import Path
from typing import Annotated
from fastapi import Depends
from src.models.connection import Connection


def get_yang_modules_path() -> Path:
    return Path("../resources/yang-modules")


YangModulesPath = Annotated[Path, Depends(get_yang_modules_path)]


class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None


connection_manager = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    return connection_manager


ConnManager = Annotated[ConnectionManager, Depends(get_connection_manager)]
