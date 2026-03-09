from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AccessListEntry(BaseModel):
    """
    The server will create an entry in this list for each
    encoding format that is supported for this stream.
    The media type 'text/event-stream' is expected
    for all event streams.  This list identifies the
    subtypes supported for this stream.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    encoding: Annotated[str, Field(alias='ietf-restconf-monitoring:encoding')]
    """
    This is the secondary encoding format within the
    'text/event-stream' encoding used by all streams.
    The type 'xml' is supported for XML encoding.
    The type 'json' is supported for JSON encoding.
    """
    location: Annotated[str, Field(alias='ietf-restconf-monitoring:location')]
    """
    Contains a URL that represents the entry point
    for establishing notification delivery via
    server-sent events.
    """


class CapabilitiesContainer(BaseModel):
    """
    Contains a list of protocol capability URIs.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    capability: Annotated[
        Optional[List[str]], Field(alias='ietf-restconf-monitoring:capability')
    ] = []
    """
    A RESTCONF protocol capability URI.
    """


class StreamListEntry(BaseModel):
    """
    Each entry describes an event stream supported by
    the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    name: Annotated[str, Field(alias='ietf-restconf-monitoring:name')]
    """
    The stream name.
    """
    description: Annotated[
        Optional[str], Field(alias='ietf-restconf-monitoring:description')
    ] = None
    """
    Description of stream content.
    """
    replay_support: Annotated[
        Optional[bool], Field(alias='ietf-restconf-monitoring:replay-support')
    ] = False
    """
    Indicates if replay buffer is supported for this stream.
    If 'true', then the server MUST support the 'start-time'
    and 'stop-time' query parameters for this stream.
    """
    replay_log_creation_time: Annotated[
        Optional[str],
        Field(
            alias='ietf-restconf-monitoring:replay-log-creation-time',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ] = None
    """
    Indicates the time the replay log for this stream
    was created.
    """
    access: Annotated[
        Optional[List[AccessListEntry]],
        Field(default_factory=list, alias='ietf-restconf-monitoring:access'),
    ]


class StreamsContainer(BaseModel):
    """
    Container representing the notification event streams
    supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    stream: Annotated[
        Optional[List[StreamListEntry]],
        Field(default_factory=list, alias='ietf-restconf-monitoring:stream'),
    ]


class RestconfStateContainer(BaseModel):
    """
    Contains RESTCONF protocol monitoring information.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    capabilities: Annotated[
        Optional[CapabilitiesContainer],
        Field(alias='ietf-restconf-monitoring:capabilities'),
    ] = None
    streams: Annotated[
        Optional[StreamsContainer], Field(alias='ietf-restconf-monitoring:streams')
    ] = None


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
        'urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring'
    )
    prefix: ClassVar[Optional[str]] = 'rcmon'
    restconf_state: Annotated[
        Optional[RestconfStateContainer],
        Field(alias='ietf-restconf-monitoring:restconf-state'),
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