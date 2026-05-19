from enum import StrEnum, auto

from pydantic import BaseModel


class ModuleStatus(StrEnum):
    REMOTE = auto()
    LOCAL = auto()


class ModuleSummary(BaseModel):
    name: str
    status: ModuleStatus
    revision: str = ""
