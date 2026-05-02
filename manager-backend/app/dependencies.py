from typing import final

from wireup import injectable

from app.models.connection import Connection


@injectable
@final
class ConnectionManager:
    def __init__(self):
        self.connection: Connection | None = None


connection_manager: ConnectionManager
