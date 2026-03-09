from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StreamListEntry(BaseModel):
    """
    Stream name, description and other information.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:netmod:notification'
    prefix: ClassVar[Optional[str]] = 'manageEvent'
    name: Annotated[str, Field(alias='nc-notifications:name')]
    """
    The name of the event stream. If this is the default
    NETCONF stream, this must have the value 'NETCONF'.
    """
    description: Annotated[str, Field(alias='nc-notifications:description')]
    """
    A description of the event stream, including such
    information as the type of events that are sent over
    this stream.
    """
    replay_support: Annotated[bool, Field(alias='nc-notifications:replaySupport')]
    """
    A description of the event stream, including such
    information as the type of events that are sent over
    this stream.
    """
    replay_log_creation_time: Annotated[
        Optional[str],
        Field(
            alias='nc-notifications:replayLogCreationTime',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ] = None
    """
    The timestamp of the creation of the log used to support
    the replay function on this stream. Note that this might
    be earlier then the earliest available notification in
    the log. This object is updated if the log resets for
    some reason.  This object MUST be present if replay is
    supported.
    """
    replay_log_aged_time: Annotated[
        Optional[str],
        Field(
            alias='nc-notifications:replayLogAgedTime',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ] = None
    """
    The timestamp of the last notification
    aged out of the log. This
    object MUST be present if replay is
    supported and any notifications
    have been aged out of the log.
    """


class StreamsContainer(BaseModel):
    """
    The list of event streams supported by the system. When
    a query is issued, the returned set of streams is
    determined based on user privileges.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:netmod:notification'
    prefix: ClassVar[Optional[str]] = 'manageEvent'
    stream: Annotated[
        Optional[List[StreamListEntry]],
        Field(default_factory=list, alias='nc-notifications:stream'),
    ]


class NetconfContainer(BaseModel):
    """
    Top-level element in the notification namespace
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:netmod:notification'
    prefix: ClassVar[Optional[str]] = 'manageEvent'
    streams: Annotated[
        Optional[StreamsContainer], Field(alias='nc-notifications:streams')
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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:netmod:notification'
    prefix: ClassVar[Optional[str]] = 'manageEvent'
    netconf: Annotated[
        Optional[NetconfContainer], Field(alias='nc-notifications:netconf')
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