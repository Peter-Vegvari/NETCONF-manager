from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class NodeSelectorCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    node_selector: Annotated[
        Optional[str], Field(alias='ietf-system-capabilities:node-selector')
    ] = None
    """
    Selects the data nodes for which capabilities are
    specified. The special value '/' denotes all data
    nodes in the datastore, consistent with the path
    leaf node on page 41 of [RFC8341].
    """


class PerNodeCapabilitiesListEntry(BaseModel):
    """
    Each list entry specifies capabilities for the selected
    data nodes.  The same capabilities apply to the data nodes
    in the subtree below the selected nodes.

    The system SHALL order the entries according to their
    precedence. The order of the entries MUST NOT change
    unless the underlying capabilities also change.

    Note that the longest patch matching can be achieved
    by ordering more specific matches before less
    specific ones.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    node_selection: Annotated[
        Optional[NodeSelectorCase],
        Field(alias='ietf-system-capabilities:node-selection'),
    ] = None


class DatastoreCapabilitiesListEntry(BaseModel):
    """
    Capabilities values per datastore.

    For non-NMDA servers/publishers, 'config false' data is
    considered as if it were part of the running datastore.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    datastore: Annotated[str, Field(alias='ietf-system-capabilities:datastore')]
    """
    The datastore for which capabilities are defined.
    Only one specific datastore can be specified,
    e.g., ds:conventional must not be used, as it
    represents a set of configuration datastores.
    """
    per_node_capabilities: Annotated[
        Optional[List[PerNodeCapabilitiesListEntry]],
        Field(
            default_factory=list, alias='ietf-system-capabilities:per-node-capabilities'
        ),
    ]


class SystemCapabilitiesContainer(BaseModel):
    """
    System capabilities.
    Capability values specified here at the system level
    are valid for all datastores and are used when the
    capability is not specified at the datastore level
    or for specific data nodes.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    datastore_capabilities: Annotated[
        Optional[List[DatastoreCapabilitiesListEntry]],
        Field(
            default_factory=list,
            alias='ietf-system-capabilities:datastore-capabilities',
        ),
    ]


class Model(BaseModel):
    """
    Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

    ## Tips
    Initialization:
    - all values have to be set via keyword arguments
    - if a class contains only a `root` field, it can be initialized as follows:
        - `member=MyNode(root=<value>)`
        - `member=<value>`

    Serialziation:
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    system_capabilities: Annotated[
        Optional[SystemCapabilitiesContainer],
        Field(alias='ietf-system-capabilities:system-capabilities'),
    ] = None


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)