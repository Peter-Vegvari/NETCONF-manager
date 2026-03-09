from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class AccessOperationsTypeType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern='^(create|read|update|delete|exec|\\s)*$')]
    """
    Access operation.
    """


class GroupNameTypeType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern='^(?=^[^\\*].*$).*$')]
    """
    Name of administrative group to which
    users can be assigned.
    """


class MatchallStringTypeType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern='^(?=^\\*$).*$')]
    """
    The string containing a single asterisk '*' is used
    to conceptually represent all possible values
    for the particular leaf using this data type.
    """


class NotificationCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    notification_name: Annotated[
        Optional[Union[MatchallStringTypeType, str]],
        Field(alias='ietf-netconf-acm:notification-name'),
    ] = None
    """
    This leaf matches if it has the value '*' or if its
    value equals the requested notification name.
    """


class UserNameLeafList(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=18446744073709551615, min_length=1)]
    """
    Each entry identifies the username of
    a member of the group associated with
    this entry.
    """


class EnumerationEnum(Enum):
    permit = 'permit'
    deny = 'deny'


class ActionTypeType(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum
    """
    Action taken by the server when a particular
    rule matches.
    """


class ActionLeaf(RootModel[ActionTypeType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: ActionTypeType
    """
    The access control action associated with the
    rule.  If a rule has been determined to match a
    particular request, then this object is used
    to determine whether to permit or deny the
    request.
    """


class DataNodeCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    path: Annotated[str, Field(alias='ietf-netconf-acm:path')]
    """
    Data node instance-identifier associated with the
    data node, action, or notification controlled by
    this rule.

    Configuration data or state data
    instance-identifiers start with a top-level
    data node.  A complete instance-identifier is
    required for this type of path value.

    The special value '/' refers to all possible
    datastore contents.
    """


class ExecDefaultLeaf(RootModel[ActionTypeType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: ActionTypeType
    """
    Controls whether exec access is granted if no appropriate
    rule is found for a particular protocol operation request.
    """


class GroupListEntry(BaseModel):
    """
    One NACM group entry.  This list will only contain
    configured entries, not any entries learned from
    any transport protocols.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    name: Annotated[
        str, Field(alias='ietf-netconf-acm:name', pattern='^(?=^[^\\*].*$).*$')
    ]
    """
    Group name associated with this entry.
    """
    user_name: Annotated[
        Optional[List[UserNameLeafList]],
        Field(default_factory=list, alias='ietf-netconf-acm:user-name'),
    ]
    """
    Each entry identifies the username of
    a member of the group associated with
    this entry.
    """


class GroupsContainer(BaseModel):
    """
    NETCONF access control groups.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    group: Annotated[
        Optional[List[GroupListEntry]],
        Field(default_factory=list, alias='ietf-netconf-acm:group'),
    ]


class ProtocolOperationCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    rpc_name: Annotated[
        Optional[Union[MatchallStringTypeType, str]],
        Field(alias='ietf-netconf-acm:rpc-name'),
    ] = None
    """
    This leaf matches if it has the value '*' or if
    its value equals the requested protocol operation
    name.
    """


class ReadDefaultLeaf(RootModel[ActionTypeType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: ActionTypeType
    """
    Controls whether read access is granted if
    no appropriate rule is found for a
    particular read request.
    """


class RuleListEntry(BaseModel):
    """
    One access control rule.

    Rules are processed in user-defined order until a match is
    found.  A rule matches if 'module-name', 'rule-type', and
    'access-operations' match the request.  If a rule
    matches, the 'action' leaf determines whether or not
    access is granted.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    name: Annotated[
        str,
        Field(
            alias='ietf-netconf-acm:name', max_length=18446744073709551615, min_length=1
        ),
    ]
    """
    Arbitrary name assigned to the rule.
    """
    module_name: Annotated[
        Optional[Union[MatchallStringTypeType, str]],
        Field(
            default_factory=lambda: MatchallStringTypeType('*'),
            alias='ietf-netconf-acm:module-name',
        ),
    ]
    """
    Name of the module associated with this rule.

    This leaf matches if it has the value '*' or if the
    object being accessed is defined in the module with the
    specified module name.
    """
    rule_type: Annotated[
        Optional[Union[ProtocolOperationCase, NotificationCase, DataNodeCase]],
        Field(alias='ietf-netconf-acm:rule-type'),
    ] = None
    access_operations: Annotated[
        Optional[Union[MatchallStringTypeType, AccessOperationsTypeType]],
        Field(
            default_factory=lambda: MatchallStringTypeType('*'),
            alias='ietf-netconf-acm:access-operations',
        ),
    ]
    """
    Access operations associated with this rule.

    This leaf matches if it has the value '*' or if the
    bit corresponding to the requested operation is set.
    """
    action: Annotated[ActionLeaf, Field(alias='ietf-netconf-acm:action')]
    comment: Annotated[Optional[str], Field(alias='ietf-netconf-acm:comment')] = None
    """
    A textual description of the access rule.
    """


class WriteDefaultLeaf(RootModel[ActionTypeType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: ActionTypeType
    """
    Controls whether create, update, or delete access
    is granted if no appropriate rule is found for a
    particular write request.
    """


class RuleListListEntry(BaseModel):
    """
    An ordered collection of access control rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    name: Annotated[
        str,
        Field(
            alias='ietf-netconf-acm:name', max_length=18446744073709551615, min_length=1
        ),
    ]
    """
    Arbitrary name assigned to the rule-list.
    """
    group: Annotated[
        Optional[List[Union[MatchallStringTypeType, GroupNameTypeType]]],
        Field(alias='ietf-netconf-acm:group'),
    ] = []
    """
    List of administrative groups that will be
    assigned the associated access rights
    defined by the 'rule' list.

    The string '*' indicates that all groups apply to the
    entry.
    """
    rule: Annotated[
        Optional[List[RuleListEntry]],
        Field(default_factory=list, alias='ietf-netconf-acm:rule'),
    ]


class NacmContainer(BaseModel):
    """
    Parameters for NETCONF access control model.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    enable_nacm: Annotated[
        Optional[bool], Field(alias='ietf-netconf-acm:enable-nacm')
    ] = True
    """
    Enables or disables all NETCONF access control
    enforcement.  If 'true', then enforcement
    is enabled.  If 'false', then enforcement
    is disabled.
    """
    read_default: Annotated[
        Optional[ReadDefaultLeaf],
        Field(
            default_factory=lambda: ReadDefaultLeaf('permit'),
            alias='ietf-netconf-acm:read-default',
        ),
    ]
    write_default: Annotated[
        Optional[WriteDefaultLeaf],
        Field(
            default_factory=lambda: WriteDefaultLeaf('deny'),
            alias='ietf-netconf-acm:write-default',
        ),
    ]
    exec_default: Annotated[
        Optional[ExecDefaultLeaf],
        Field(
            default_factory=lambda: ExecDefaultLeaf('permit'),
            alias='ietf-netconf-acm:exec-default',
        ),
    ]
    enable_external_groups: Annotated[
        Optional[bool], Field(alias='ietf-netconf-acm:enable-external-groups')
    ] = True
    """
    Controls whether the server uses the groups reported by the
    NETCONF transport layer when it assigns the user to a set of
    NACM groups.  If this leaf has the value 'false', any group
    names reported by the transport layer are ignored by the
    server.
    """
    denied_operations: Annotated[
        Optional[int],
        Field(alias='ietf-netconf-acm:denied-operations', ge=0, le=4294967295),
    ] = 0
    """
    Number of times since the server last restarted that a
    protocol operation request was denied.
    """
    denied_data_writes: Annotated[
        Optional[int],
        Field(alias='ietf-netconf-acm:denied-data-writes', ge=0, le=4294967295),
    ] = 0
    """
    Number of times since the server last restarted that a
    protocol operation request to alter
    a configuration datastore was denied.
    """
    denied_notifications: Annotated[
        Optional[int],
        Field(alias='ietf-netconf-acm:denied-notifications', ge=0, le=4294967295),
    ] = 0
    """
    Number of times since the server last restarted that
    a notification was dropped for a subscription because
    access to the event type was denied.
    """
    groups: Annotated[
        Optional[GroupsContainer], Field(alias='ietf-netconf-acm:groups')
    ] = None
    rule_list: Annotated[
        Optional[List[RuleListListEntry]],
        Field(default_factory=list, alias='ietf-netconf-acm:rule-list'),
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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    prefix: ClassVar[Optional[str]] = 'nacm'
    nacm: Annotated[Optional[NacmContainer], Field(alias='ietf-netconf-acm:nacm')] = (
        None
    )


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