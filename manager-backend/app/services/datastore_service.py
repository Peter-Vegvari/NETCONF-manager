from typing import Any, cast

import app.dependencies
from app.models.datastore import DataStore

_LOCK_INFO_FILTER = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <datastores/>
    </netconf-state>
"""
_MON_NS = "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"


def _session() -> Any:
    s = app.dependencies.connection_manager.session
    assert s is not None
    return cast(Any, s)


def copy_config(source: DataStore, target: DataStore) -> str:
    reply = _session().copy_config(source=source.value, target=target.value)
    return cast(str, reply.xml)


def delete_config(data_store: DataStore) -> str:
    reply = _session().delete_config(target=data_store.value)
    return cast(str, reply.xml)


def lock(data_store: DataStore) -> str:
    reply = _session().lock(target=data_store.value)
    return cast(str, reply.xml)


def unlock(data_store: DataStore) -> str:
    reply = _session().unlock(target=data_store.value)
    return cast(str, reply.xml)


def is_locked(data_store: DataStore) -> bool:
    reply = _session().get(filter=("subtree", _LOCK_INFO_FILTER))
    for ds in reply.data_ele.iter(f"{{{_MON_NS}}}datastore"):
        if ds.findtext(f"{{{_MON_NS}}}name") == data_store.value:
            return ds.find(f"{{{_MON_NS}}}locks") is not None
    return False
