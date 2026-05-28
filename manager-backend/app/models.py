from enum import StrEnum, auto

from ncclient import manager
from ncclient.manager import Manager
from pydantic import BaseModel


class Connection(BaseModel):
    host: str
    port: int
    user_name: str
    password: str

    def connect(self) -> Manager:
        result = manager.connect(
            host=self.host,
            port=self.port,
            username=self.user_name,
            password=self.password,
            hostkey_verify=False,
            device_params={"name": "default"},
            allow_agent=False,
            look_for_keys=False,
            timeout=10,
        )
        assert result is not None
        return result


class DataStore(StrEnum):
    STARTUP = "startup"
    CANDIDATE = "candidate"
    RUNNING = "running"


class ModuleStatus(StrEnum):
    REMOTE = auto()
    LOCAL = auto()


class ModuleSummary(BaseModel):
    name: str
    status: ModuleStatus
    revision: str = ""


class SchemaNode(BaseModel):
    kind: str | None = None
    config: bool | None = None
    description: str | None = None
    mandatory: bool | None = None
    default: object | None = None
    type: dict[str, object] | None = None
    children: dict[str, "SchemaNode"] | None = None
