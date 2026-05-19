from enum import StrEnum


class DataStore(StrEnum):
    STARTUP = "startup"
    CANDIDATE = "candidate"
    RUNNING = "running"
