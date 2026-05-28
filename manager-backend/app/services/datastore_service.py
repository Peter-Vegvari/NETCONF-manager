from typing import Any, cast

import app.services.connection_service
from app.models import DataStore
from app.services import module_service

_LOCK_INFO_FILTER = """
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
        <datastores/>
    </netconf-state>
"""
_MON_NS = "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"


def edit_config(data_store: DataStore, module_name: str, path: str, value: str) -> None:
    ns = module_service.get_namespace(module_name)
    if not ns:
        ns = f"urn:ietf:params:xml:ns:yang:{module_name}"
    parts = path.strip("/").split("/")
    root_tag = parts[0]
    inner_content = value
    for tag in reversed(parts[1:]):
        inner_content = f"<{tag}>{inner_content}</{tag}>"
    config_xml = (
        f'<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'
        f'<{root_tag} xmlns="{ns}">{inner_content}</{root_tag}>'
        f"</config>"
    )
    app.services.connection_service.connection_manager.session.edit_config(
        target=data_store.value, config=config_xml
    )


def copy_config(source: DataStore, target: DataStore) -> None:
    app.services.connection_service.connection_manager.session.copy_config(
        source=source.value, target=target.value
    )


def delete_config(data_store: DataStore) -> None:
    app.services.connection_service.connection_manager.session.delete_config(
        target=data_store.value
    )


def lock(data_store: DataStore) -> None:
    app.services.connection_service.connection_manager.session.lock(
        target=data_store.value
    )


def unlock(data_store: DataStore) -> None:
    app.services.connection_service.connection_manager.session.unlock(
        target=data_store.value
    )


def is_locked(data_store: DataStore) -> bool:
    reply = cast(
        Any,
        app.services.connection_service.connection_manager.session.get(
            filter=("subtree", _LOCK_INFO_FILTER)
        ),
    )
    for ds in reply.data_ele.iter(f"{{{_MON_NS}}}datastore"):
        if ds.findtext(f"{{{_MON_NS}}}name") == data_store.value:
            return ds.find(f"{{{_MON_NS}}}locks") is not None
    return False


def commit() -> None:
    app.services.connection_service.connection_manager.session.commit()
