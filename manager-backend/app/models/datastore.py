from enum import StrEnum

from pydantic import BaseModel


class DataStore(StrEnum):
    STARTUP = "startup"
    CANDIDATE = "candidate"
    RUNNING = "running"


class EditConfigRequest(BaseModel):
    module_name: str
    path: str
    value: str
