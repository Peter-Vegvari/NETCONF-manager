from typing import Any, cast, final

from ncclient.manager import Manager
from wireup import injectable

from app.models.connection import Connection


@injectable
@final
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None
        self._session: Manager | None = None

    def _is_connected(self, session: Manager) -> bool:
        return cast(bool, session.connected)

    @property
    def session(self) -> Manager | None:
        if self._session and self._is_connected(self._session):
            return self._session
        if self.connection:
            self._session = self.connection.connect()
            return self._session
        return None

    def connect(self, connection: Connection) -> Manager:
        self.disconnect()
        self.connection = connection
        self._session = connection.connect()
        return self._session

    def disconnect(self) -> None:
        if self._session and self._is_connected(self._session):
            cast(Any, self._session).close_session()
        self._session = None
        self.connection = None


connection_manager: ConnectionManager
