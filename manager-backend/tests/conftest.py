from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app.dependencies
from app.core.config import settings
from app.dependencies import ConnectionManager
from app.main import app


@pytest.fixture
def tmp_modules_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def client(tmp_modules_dir: Path) -> Iterator[TestClient]:
    original_path = settings.DOWNLOADED_MODULES_PATH
    settings.DOWNLOADED_MODULES_PATH = tmp_modules_dir

    cm = ConnectionManager.__new__(ConnectionManager)
    cm.connection = None
    app.dependencies.connection_manager = cm

    with TestClient(app) as c:
        yield c

    settings.DOWNLOADED_MODULES_PATH = original_path
