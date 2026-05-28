from typing import Any, cast, final

from fastapi import HTTPException
from ncclient.manager import Manager
from wireup import injectable

from app.models import Connection


@injectable
@final
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None
        self._session: Manager | None = None

    @property
    def is_connected(self) -> bool:
        return cast(bool, self._session.connected) if self._session else False

    @property
    def session(self) -> Manager:
        if self.is_connected:
            assert self._session is not None
            return self._session
        if self.connection:
            try:
                self._session = self.connection.connect()
            except Exception:
                self._session = None
        assert self._session is not None
        return self._session

    def check_connected(self) -> None:
        if not self.is_connected:
            raise HTTPException(400, "Not connected")

    def connect(self, connection: Connection) -> Manager:
        self.disconnect()
        self.connection = connection
        try:
            self._session = connection.connect()
        except Exception:
            self.connection = None
            raise
        return self._session

    def disconnect(self) -> None:
        if self.is_connected:
            cast(Any, self._session).close_session()
        self._session = None
        self.connection = None


connection_manager: ConnectionManager
