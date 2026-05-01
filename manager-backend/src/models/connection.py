import os
from pathlib import Path

from lxml import etree
from ncclient import manager
from ncclient.manager import Manager
from pydantic import BaseModel


class Connection(BaseModel):
    host: str
    port: int
    user_name: str
    password: str

    def connect(self) -> Manager:
        return manager.connect(
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
