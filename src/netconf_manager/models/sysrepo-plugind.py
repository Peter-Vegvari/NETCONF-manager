from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EnabledContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    older_than: Annotated[
        str,
        Field(
            alias='sysrepo-plugind:older-than', pattern='^(?=^[1-9][0-9]*[smhDWMY]$).*$'
        ),
    ]
    """
    Period that has to elapse for notifications to be rotated. Units can be
    [s] seconds, [m] minutes, [h] hours, [D] days, [W] weeks, [M] months,
    or [Y] years.
    """
    output_dir: Annotated[str, Field(alias='sysrepo-plugind:output-dir')]
    """
    Contains rotated notifications.
    """
    compress: Annotated[Optional[bool], Field(alias='sysrepo-plugind:compress')] = True
    """
    Enable/disable compression of rotated notifications with zip,
    if disabled then notifications are simply copied to the output folder.
    """


class LoadedPluginsContainer(BaseModel):
    """
    Names of all the loaded (initialized) plugins.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    plugin: Annotated[Optional[List[str]], Field(alias='sysrepo-plugind:plugin')] = []
    """
    Name of a loaded plugin.
    """


class PluginOrderContainer(BaseModel):
    """
    The order in which to run plugins from the sysrepo-plugind.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    plugin: Annotated[Optional[List[str]], Field(alias='sysrepo-plugind:plugin')] = []
    """
    The name of the plugin file, which may or may not include the extension.
    """


class PollDiffSubscriptionListEntry(BaseModel):
    """
    Subscription periodically retrieving data of an operational get subscription
    and reporting changes to any subscribers.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    module_name: Annotated[str, Field(alias='sysrepo-plugind:module-name')]
    """
    Module name of the operational get subscription to poll.
    """
    path: Annotated[str, Field(alias='sysrepo-plugind:path')]
    """
    Path of the operational get subscription to poll.
    """
    valid: Annotated[int, Field(alias='sysrepo-plugind:valid', ge=0, le=4294967295)]
    """
    Interval of data retrieval and the changes report.
    """


class RotationContainer(BaseModel):
    """
    Notification rotation configuration and statistics.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    enabled: Annotated[
        Optional[EnabledContainer], Field(alias='sysrepo-plugind:enabled')
    ] = None
    rotated_files_count: Annotated[
        Optional[int],
        Field(
            alias='sysrepo-plugind:rotated-files-count', ge=0, le=18446744073709551615
        ),
    ] = None
    """
    Number of rotated files while sysrepo-plugind is running
    """


class NotifDatastoreContainer(BaseModel):
    """
    Includes configuration for notification datastore.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    rotation: Annotated[
        Optional[RotationContainer], Field(alias='sysrepo-plugind:rotation')
    ] = None


class OperDatastoreContainer(BaseModel):
    """
    Includes configuration of operational datastore.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    poll_diff_subscription: Annotated[
        Optional[List[PollDiffSubscriptionListEntry]],
        Field(default_factory=list, alias='sysrepo-plugind:poll-diff-subscription'),
    ]


class SysrepoPlugindContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    plugin_order: Annotated[
        Optional[PluginOrderContainer], Field(alias='sysrepo-plugind:plugin-order')
    ] = None
    notif_datastore: Annotated[
        Optional[NotifDatastoreContainer],
        Field(alias='sysrepo-plugind:notif-datastore'),
    ] = None
    oper_datastore: Annotated[
        Optional[OperDatastoreContainer], Field(alias='sysrepo-plugind:oper-datastore')
    ] = None
    loaded_plugins: Annotated[
        Optional[LoadedPluginsContainer], Field(alias='sysrepo-plugind:loaded-plugins')
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
    namespace: ClassVar[Optional[str]] = 'urn:sysrepo:plugind'
    prefix: ClassVar[Optional[str]] = 'srpd'
    sysrepo_plugind: Annotated[
        Optional[SysrepoPlugindContainer],
        Field(alias='sysrepo-plugind:sysrepo-plugind'),
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