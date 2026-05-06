from typing import final

from ncclient.manager import Manager
from wireup import injectable

from app.models.connection import Connection


@injectable
@final
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None
        self._session: Manager | None = None

    @property
    def session(self) -> Manager | None:
        if self._session and self._session.connected:
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

    def disconnect(self):
        if self._session and self._session.connected:
            self._session.close_session()
        self._session = None
        self.connection = None


connection_manager: ConnectionManager
