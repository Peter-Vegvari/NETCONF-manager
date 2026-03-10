from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PublicKeyListEntry(BaseModel):
    """
    A public key.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    name: Annotated[str, Field(alias='ietf-truststore:name')]
    """
    An arbitrary name for this public key.
    """
    public_key_format: Annotated[str, Field(alias='ietf-truststore:public-key-format')]
    """
    Identifies the public key's format. Implementations SHOULD
    ensure that the incoming public key value is encoded in the
    specified format.
    """
    public_key: Annotated[
        bytes,
        Field(alias='ietf-truststore:public-key', max_length=18446744073709551615),
    ]
    """
    The binary value of the public key.  The interpretation
    of the value is defined by 'public-key-format' field.
    """


class CertificateListEntry(BaseModel):
    """
    A trust anchor certificate.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    name: Annotated[str, Field(alias='ietf-truststore:name')]
    """
    An arbitrary name for this certificate.
    """
    cert_data: Annotated[
        bytes, Field(alias='ietf-truststore:cert-data', max_length=18446744073709551615)
    ]
    """
    The binary certificate data for this certificate.
    """


class PublicKeyBagListEntry(BaseModel):
    """
    A bag of public keys.  Each bag of keys SHOULD be for
    a specific purpose.  For instance, one bag could be used
    authenticate a specific set of servers, while another
    could be used to authenticate a specific set of clients.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    name: Annotated[str, Field(alias='ietf-truststore:name')]
    """
    An arbitrary name for this bag of public keys.
    """
    description: Annotated[
        Optional[str], Field(alias='ietf-truststore:description')
    ] = None
    """
    A description for this bag public keys.  The
    intended purpose for the bag SHOULD be described.
    """
    public_key: Annotated[
        Optional[List[PublicKeyListEntry]],
        Field(default_factory=list, alias='ietf-truststore:public-key'),
    ]


class PublicKeyBagsContainer(BaseModel):
    """
    A collection of public key bags.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    public_key_bag: Annotated[
        Optional[List[PublicKeyBagListEntry]],
        Field(default_factory=list, alias='ietf-truststore:public-key-bag'),
    ]


class CertificateBagListEntry(BaseModel):
    """
    A bag of certificates.  Each bag of certificates SHOULD
    be for a specific purpose.  For instance, one bag could
    be used to authenticate a specific set of servers, while
    another could be used to authenticate a specific set of
    clients.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    name: Annotated[str, Field(alias='ietf-truststore:name')]
    """
    An arbitrary name for this bag of certificates.
    """
    description: Annotated[
        Optional[str], Field(alias='ietf-truststore:description')
    ] = None
    """
    A description for this bag of certificates.  The
    intended purpose for the bag SHOULD be described.
    """
    certificate: Annotated[
        Optional[List[CertificateListEntry]],
        Field(default_factory=list, alias='ietf-truststore:certificate'),
    ]


class CertificateBagsContainer(BaseModel):
    """
    A collection of certificate bags.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    certificate_bag: Annotated[
        Optional[List[CertificateBagListEntry]],
        Field(default_factory=list, alias='ietf-truststore:certificate-bag'),
    ]


class TruststoreContainer(BaseModel):
    """
    The truststore contains bags of certificates and
    public keys.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    certificate_bags: Annotated[
        Optional[CertificateBagsContainer],
        Field(alias='ietf-truststore:certificate-bags'),
    ] = None
    public_key_bags: Annotated[
        Optional[PublicKeyBagsContainer], Field(alias='ietf-truststore:public-key-bags')
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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-truststore'
    prefix: ClassVar[Optional[str]] = 'ts'
    truststore: Annotated[
        Optional[TruststoreContainer], Field(alias='ietf-truststore:truststore')
    ] = None
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
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer(BaseModel):
    """
    A container for a list of key exchange algorithms
    supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:iana-ssh-key-exchange-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshkea'
    supported_algorithm: Annotated[
        Optional[List[str]],
        Field(alias='iana-ssh-key-exchange-algs:supported-algorithm'),
    ] = []
    """
    A key exchange algorithm supported by the server.
    """


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
        'urn:ietf:params:xml:ns:yang:iana-ssh-key-exchange-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshkea'
    supported_algorithms: Annotated[
        Optional[SupportedAlgorithmsContainer],
        Field(alias='iana-ssh-key-exchange-algs:supported-algorithms'),
    ] = None
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer2(BaseModel):
    """
    A container for a list of encryption algorithms
    supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:iana-ssh-encryption-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshea'
    supported_algorithm: Annotated[
        Optional[List[str]], Field(alias='iana-ssh-encryption-algs:supported-algorithm')
    ] = []
    """
    A encryption algorithm supported by the server.
    """


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
        'urn:ietf:params:xml:ns:yang:iana-ssh-encryption-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshea'
    supported_algorithms: Annotated[
        Optional[SupportedAlgorithmsContainer2],
        Field(alias='iana-ssh-encryption-algs:supported-algorithms'),
    ] = None
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer3(BaseModel):
    """
    A container for a list of cipher suite algorithms supported
    by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:iana-tls-cipher-suite-algs'
    )
    prefix: ClassVar[Optional[str]] = 'tlscsa'
    supported_algorithm: Annotated[
        Optional[List[str]],
        Field(alias='iana-tls-cipher-suite-algs:supported-algorithm'),
    ] = []
    """
    A cipher suite algorithm supported by the server.
    """


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
        'urn:ietf:params:xml:ns:yang:iana-tls-cipher-suite-algs'
    )
    prefix: ClassVar[Optional[str]] = 'tlscsa'
    supported_algorithms: Annotated[
        Optional[SupportedAlgorithmsContainer3],
        Field(alias='iana-tls-cipher-suite-algs:supported-algorithms'),
    ] = None
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
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer4(BaseModel):
    """
    A container for a list of public key algorithms
    supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:iana-ssh-public-key-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshpka'
    supported_algorithm: Annotated[
        Optional[List[str]], Field(alias='iana-ssh-public-key-algs:supported-algorithm')
    ] = []
    """
    A public key algorithm supported by the server.
    """


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
        'urn:ietf:params:xml:ns:yang:iana-ssh-public-key-algs'
    )
    prefix: ClassVar[Optional[str]] = 'sshpka'
    supported_algorithms: Annotated[
        Optional[SupportedAlgorithmsContainer4],
        Field(alias='iana-ssh-public-key-algs:supported-algorithms'),
    ] = None
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer5(BaseModel):
    """
    A container for a list of MAC algorithms
    supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:iana-ssh-mac-algs'
    prefix: ClassVar[Optional[str]] = 'sshma'
    supported_algorithm: Annotated[
        Optional[List[str]], Field(alias='iana-ssh-mac-algs:supported-algorithm')
    ] = []
    """
    A MAC algorithm supported by the server.
    """


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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:iana-ssh-mac-algs'
    prefix: ClassVar[Optional[str]] = 'sshma'
    supported_algorithms: Annotated[
        Optional[SupportedAlgorithmsContainer5],
        Field(alias='iana-ssh-mac-algs:supported-algorithms'),
    ] = None
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class InlineContainer(BaseModel):
    """
    This node indicates that the server has mounted at least
    the module 'ietf-yang-library' at the mount point, and
    its instantiation provides the information about the
    mounted schema.

    Different instances of the mount point may have
    different schemas mounted.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'


class SharedSchemaContainer(BaseModel):
    """
    This node indicates that the server has mounted at least
    the module 'ietf-yang-library' at the mount point, and
    its instantiation provides the information about the
    mounted schema.  When XPath expressions in the mounted
    schema are evaluated, the 'parent-reference' leaf-list
    is taken into account.

    Different instances of the mount point MUST have the
    same schema mounted.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    parent_reference: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-schema-mount:parent-reference')
    ] = []
    """
    Entries of this leaf-list are XPath 1.0 expressions
    that are evaluated in the following context:

    - The context node is the node in the parent data tree
      where the mount-point is defined.

    - The accessible tree is the parent data tree
      *without* any nodes defined in modules that are
      mounted inside the parent schema.

    - The context position and context size are both equal
      to 1.

    - The set of variable bindings is empty.

    - The function library is the core function library
      defined in the W3C XPath 1.0 document
      (http://www.w3.org/TR/1999/REC-xpath-19991116) and
      the functions defined in Section 10 of RFC 7950.

    - The set of namespace declarations is defined by the
      'namespace' list under 'schema-mounts'.

    Each XPath expression MUST evaluate to a node-set
    (possibly empty).  For the purposes of evaluating
    XPath expressions whose context nodes are defined in
    the mounted schema, the union of all these node-sets
    together with ancestor nodes are added to the
    accessible data tree.

    Note that in the case 'ietf-yang-schema-mount' is
    itself mounted, a 'parent-reference' in the mounted
    module may refer to nodes that were brought into the
    accessible tree through a 'parent-reference' in the
    parent schema.
    """


class InlineCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    inline: Annotated[
        Optional[InlineContainer], Field(alias='ietf-yang-schema-mount:inline')
    ] = None


class SharedSchemaCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    shared_schema: Annotated[
        Optional[SharedSchemaContainer],
        Field(alias='ietf-yang-schema-mount:shared-schema'),
    ] = None


class MountPointListEntry(BaseModel):
    """
    Each entry of this list specifies a schema for a particular
    mount point.

    Each mount point MUST be defined using the 'mount-point'
    extension in one of the modules listed in the server's
    YANG library instance with conformance type 'implement'.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    module: Annotated[
        str,
        Field(
            alias='ietf-yang-schema-mount:module',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    Name of a module containing the mount point.
    """
    label: Annotated[
        str,
        Field(
            alias='ietf-yang-schema-mount:label',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    Label of the mount point defined using the 'mount-point'
    extension.
    """
    config: Annotated[Optional[bool], Field(alias='ietf-yang-schema-mount:config')] = (
        True
    )
    """
    If this leaf is set to 'false', then all data nodes in the
    mounted schema are read-only ('config false'), regardless
    of their 'config' property.
    """
    schema_ref: Annotated[
        Union[InlineCase, SharedSchemaCase],
        Field(alias='ietf-yang-schema-mount:schema-ref'),
    ]


class NamespaceListEntry(BaseModel):
    """
    This list provides a mapping of namespace prefixes that are
    used in XPath expressions of 'parent-reference' leafs to the
    corresponding namespace URI references.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: Annotated[
        str,
        Field(
            alias='ietf-yang-schema-mount:prefix',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    Namespace prefix.
    """
    uri: Annotated[Optional[str], Field(alias='ietf-yang-schema-mount:uri')] = None
    """
    Namespace URI reference.
    """


class SchemaMountsContainer(BaseModel):
    """
    Contains information about the structure of the overall
    mounted data model implemented in the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: Annotated[
        Optional[List[NamespaceListEntry]],
        Field(default_factory=list, alias='ietf-yang-schema-mount:namespace'),
    ]
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    mount_point: Annotated[
        Optional[List[MountPointListEntry]],
        Field(default_factory=list, alias='ietf-yang-schema-mount:mount-point'),
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
        'urn:ietf:params:xml:ns:yang:ietf-yang-schema-mount'
    )
    prefix: ClassVar[Optional[str]] = 'yangmnt'
    schema_mounts: Annotated[
        Optional[SchemaMountsContainer],
        Field(alias='ietf-yang-schema-mount:schema-mounts'),
    ] = None
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
from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class SupportedUpdatePeriodLeafList(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=4294967295)]
    """
    Supported update period values for a 'periodic'
    subscription.

    A subscription request to the selected data nodes with a
    period not included in the leaf-list will result in a
    'period-unsupported' error.
    """


class SupportedUpdatePeriodLeafList2(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=4294967295)]
    """
    Supported update period values for a 'periodic'
    subscription.

    A subscription request to the selected data nodes with a
    period not included in the leaf-list will result in a
    'period-unsupported' error.
    """


class EnumerationEnum2(Enum):
    none = 'none'
    all = 'all'


class EnumerationEnum3(Enum):
    create = 'create'
    delete = 'delete'
    insert = 'insert'
    move = 'move'
    replace = 'replace'


class EnumerationEnum4(Enum):
    none = 'none'
    all = 'all'


class ChangeTypeType(RootModel[EnumerationEnum3]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum3
    """
    Specifies different types of datastore changes.

    This type is based on the edit operations defined for
    YANG Patch, with the difference that it is valid for a
    receiver to process an update record that performs a
    'create' operation on a datastore node the receiver believes
    exists or to process a delete on a datastore node the
    receiver believes is missing.
    """


class MinimumUpdatePeriodCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    minimum_update_period: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:minimum-update-period',
            ge=0,
            le=4294967295,
        ),
    ] = None
    """
    Indicates the minimal update period that is
    supported for a 'periodic' subscription.

    A subscription request to the selected data nodes with
    a smaller period than what this leaf specifies is
    likely to result in a 'period-unsupported' error.
    """


class MinimumUpdatePeriodCase2(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    minimum_update_period: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:minimum-update-period',
            ge=0,
            le=4294967295,
        ),
    ] = None
    """
    Indicates the minimal update period that is
    supported for a 'periodic' subscription.

    A subscription request to the selected data nodes with
    a smaller period than what this leaf specifies is
    likely to result in a 'period-unsupported' error.
    """


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


class SupportedUpdatePeriodCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    supported_update_period: Annotated[
        Optional[List[SupportedUpdatePeriodLeafList]],
        Field(
            default_factory=list,
            alias='ietf-notification-capabilities:supported-update-period',
        ),
    ]
    """
    Supported update period values for a 'periodic'
    subscription.

    A subscription request to the selected data nodes with a
    period not included in the leaf-list will result in a
    'period-unsupported' error.
    """


class SupportedUpdatePeriodCase2(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    supported_update_period: Annotated[
        Optional[List[SupportedUpdatePeriodLeafList2]],
        Field(
            default_factory=list,
            alias='ietf-notification-capabilities:supported-update-period',
        ),
    ]
    """
    Supported update period values for a 'periodic'
    subscription.

    A subscription request to the selected data nodes with a
    period not included in the leaf-list will result in a
    'period-unsupported' error.
    """


class SubscriptionCapabilitiesContainer(BaseModel):
    """
    Capabilities related to YANG-Push subscriptions
    and notifications
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    max_nodes_per_update: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:max-nodes-per-update',
            ge=1,
            le=4294967295,
        ),
    ] = None
    """
    Maximum number of data nodes that can be sent
    in an update. The publisher MAY support more data nodes
    but SHOULD support at least this number.

    May be used to avoid the 'update-too-big' error
    during subscription.
    """
    periodic_notifications_supported: Annotated[
        Optional[str],
        Field(
            alias='ietf-notification-capabilities:periodic-notifications-supported',
            pattern='^(config-changes|state-changes|\\s)*$',
        ),
    ] = None
    """
    Specifies whether the publisher is capable of
    sending 'periodic' notifications for the selected
    data nodes, including any subtrees that may exist
    below them.
    """
    update_period: Annotated[
        Optional[Union[MinimumUpdatePeriodCase, SupportedUpdatePeriodCase]],
        Field(alias='ietf-notification-capabilities:update-period'),
    ] = None
    on_change_supported: Annotated[
        Optional[str],
        Field(
            alias='ietf-notification-capabilities:on-change-supported',
            pattern='^(config-changes|state-changes|\\s)*$',
        ),
    ] = None
    """
    Specifies whether the publisher is capable of
    sending 'on-change' notifications for the selected
    data nodes and the subtree below them.
    """
    minimum_dampening_period: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:minimum-dampening-period',
            ge=0,
            le=4294967295,
        ),
    ] = None
    """
    The minimum dampening period supported for 'on-change'
    subscriptions for the selected data nodes.

    If this value is present and greater than zero,
    that implies dampening is mandatory.
    """
    supported_excluded_change_type: Annotated[
        Optional[List[Union[EnumerationEnum2, ChangeTypeType]]],
        Field(alias='ietf-notification-capabilities:supported-excluded-change-type'),
    ] = ['none']
    """
    The change types that can be excluded in
    YANG-Push subscriptions for the selected data nodes.
    """


class SubscriptionCapabilitiesContainer2(BaseModel):
    """
    Capabilities related to YANG-Push subscriptions
    and notifications
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:yang:ietf-notification-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'notc'
    max_nodes_per_update: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:max-nodes-per-update',
            ge=1,
            le=4294967295,
        ),
    ] = None
    """
    Maximum number of data nodes that can be sent
    in an update. The publisher MAY support more data nodes
    but SHOULD support at least this number.

    May be used to avoid the 'update-too-big' error
    during subscription.
    """
    periodic_notifications_supported: Annotated[
        Optional[str],
        Field(
            alias='ietf-notification-capabilities:periodic-notifications-supported',
            pattern='^(config-changes|state-changes|\\s)*$',
        ),
    ] = None
    """
    Specifies whether the publisher is capable of
    sending 'periodic' notifications for the selected
    data nodes, including any subtrees that may exist
    below them.
    """
    update_period: Annotated[
        Optional[Union[MinimumUpdatePeriodCase2, SupportedUpdatePeriodCase2]],
        Field(alias='ietf-notification-capabilities:update-period'),
    ] = None
    on_change_supported: Annotated[
        Optional[str],
        Field(
            alias='ietf-notification-capabilities:on-change-supported',
            pattern='^(config-changes|state-changes|\\s)*$',
        ),
    ] = None
    """
    Specifies whether the publisher is capable of
    sending 'on-change' notifications for the selected
    data nodes and the subtree below them.
    """
    minimum_dampening_period: Annotated[
        Optional[int],
        Field(
            alias='ietf-notification-capabilities:minimum-dampening-period',
            ge=0,
            le=4294967295,
        ),
    ] = None
    """
    The minimum dampening period supported for 'on-change'
    subscriptions for the selected data nodes.

    If this value is present and greater than zero,
    that implies dampening is mandatory.
    """
    supported_excluded_change_type: Annotated[
        Optional[List[Union[EnumerationEnum4, ChangeTypeType]]],
        Field(alias='ietf-notification-capabilities:supported-excluded-change-type'),
    ] = ['none']
    """
    The change types that can be excluded in
    YANG-Push subscriptions for the selected data nodes.
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
    subscription_capabilities: Annotated[
        Optional[SubscriptionCapabilitiesContainer],
        Field(alias='ietf-notification-capabilities:subscription-capabilities'),
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
    subscription_capabilities: Annotated[
        Optional[SubscriptionCapabilitiesContainer2],
        Field(alias='ietf-notification-capabilities:subscription-capabilities'),
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
        'urn:ietf:params:xml:ns:yang:ietf-system-capabilities'
    )
    prefix: ClassVar[Optional[str]] = 'sysc'
    system_capabilities: Annotated[
        Optional[SystemCapabilitiesContainer],
        Field(alias='ietf-system-capabilities:system-capabilities'),
    ] = None
from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class RevisionIdentifierType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern='^(?=^\\d{4}-\\d{2}-\\d{2}$).*$')]
    """
    Represents a specific date in YYYY-MM-DD format.
    """


class RevisionLeaf31(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=0, min_length=0)]
    """
    The YANG module revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module.
    """


class RevisionLeaf51(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=0, min_length=0)]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """


class RevisionLeaf61(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=0, min_length=0)]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """


class RevisionLeaf71(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=0, min_length=0)]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """


class EnumerationEnum5(Enum):
    implement = 'implement'
    import_ = 'import'


class ConformanceTypeLeaf(RootModel[EnumerationEnum5]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum5
    """
    Indicates the type of conformance the server is claiming
    for the YANG module identified by this entry.
    """


class DatastoreListEntry(BaseModel):
    """
    A datastore supported by this server.

    Each datastore indicates which schema it supports.

    The server MUST instantiate one entry in this list per
    specific datastore it supports.
    Each datastore entry with the same datastore schema SHOULD
    reference the same schema.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[str, Field(alias='ietf-yang-library:name')]
    """
    The identity of the datastore.
    """
    schema: Annotated[str, Field(alias='ietf-yang-library:schema')]
    """
    A reference to the schema supported by this datastore.
    All non-import-only modules of the schema are implemented
    with their associated features and deviations.
    """


class FeatureLeafList(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$'
        ),
    ]
    """
    List of all YANG feature names from this module that are
    supported by the server, regardless whether they are defined
    in the module or any included submodule.
    """


class FeatureLeafList2(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$'
        ),
    ]
    """
    List of YANG feature names from this module that are
    supported by the server, regardless of whether they are
    defined in the module or any included submodule.
    """


class SchemaListEntry(BaseModel):
    """
    A datastore schema that may be used by one or more
    datastores.

    The schema must be valid and referentially complete, i.e.,
    it must contain modules to satisfy all used import
    statements for all modules specified in the schema.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[str, Field(alias='ietf-yang-library:name')]
    """
    An arbitrary name of the schema.
    """
    module_set: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-library:module-set')
    ] = []
    """
    A set of module-sets that are included in this schema.
    If a non-import-only module appears in multiple module
    sets, then the module revision and the associated features
    and deviations must be identical.
    """


class SubmoduleListEntry(BaseModel):
    """
    Each entry represents one submodule within the
    parent module.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Optional[str],
        Field(
            alias='ietf-yang-library:revision', pattern='^(?=^\\d{4}-\\d{2}-\\d{2}$).*$'
        ),
    ] = None
    """
    The YANG module or submodule revision date.  If no revision
    statement is present in the YANG module or submodule, this
    leaf is not instantiated.
    """
    location: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-library:location')
    ] = []
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """


class SubmoduleListEntry2(BaseModel):
    """
    Each entry represents one submodule within the
    parent module.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Optional[str],
        Field(
            alias='ietf-yang-library:revision', pattern='^(?=^\\d{4}-\\d{2}-\\d{2}$).*$'
        ),
    ] = None
    """
    The YANG module or submodule revision date.  If no revision
    statement is present in the YANG module or submodule, this
    leaf is not instantiated.
    """
    location: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-library:location')
    ] = []
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """


class SubmoduleListEntry3(BaseModel):
    """
    Each entry represents one submodule within the
    parent module.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Union[RevisionIdentifierType, RevisionLeaf71],
        Field(alias='ietf-yang-library:revision'),
    ]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """
    schema: Annotated[Optional[str], Field(alias='ietf-yang-library:schema')] = None
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """


class DeviationLeafList(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$'
        ),
    ]
    """
    List of all YANG deviation modules used by this server to
    modify the conformance of the module associated with this
    entry.  Note that the same module can be used for deviations
    for multiple modules, so the same entry MAY appear within
    multiple 'module' entries.

    This reference MUST NOT (directly or indirectly)
    refer to the module being deviated.

    Robust clients may want to make sure that they handle a
    situation where a module deviates itself (directly or
    indirectly) gracefully.
    """


class DeviationListEntry(BaseModel):
    """
    List of YANG deviation module names and revisions
    used by this server to modify the conformance of
    the module associated with this entry.  Note that
    the same module can be used for deviations for
    multiple modules, so the same entry MAY appear
    within multiple 'module' entries.

    The deviation module MUST be present in the 'module'
    list, with the same name and revision values.
    The 'conformance-type' value will be 'implement' for
    the deviation module.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Union[RevisionIdentifierType, RevisionLeaf61],
        Field(alias='ietf-yang-library:revision'),
    ]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """


class ImportOnlyModuleListEntry(BaseModel):
    """
    An entry in this list indicates that the server imports
    reusable definitions from the specified revision of the
    module but does not implement any protocol-accessible
    objects from this revision.

    Multiple entries for the same module name MAY exist.  This
    can occur if multiple modules import the same module but
    specify different revision dates in the import statements.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: Annotated[str, Field(alias='ietf-yang-library:namespace')]
    """
    The XML namespace identifier for this module.
    """
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module name.
    """
    revision: Annotated[
        Union[RevisionIdentifierType, RevisionLeaf31],
        Field(alias='ietf-yang-library:revision'),
    ]
    """
    The YANG module revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module.
    """
    location: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-library:location')
    ] = []
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """
    submodule: Annotated[
        Optional[List[SubmoduleListEntry2]],
        Field(default_factory=list, alias='ietf-yang-library:submodule'),
    ]


class ModuleListEntry(BaseModel):
    """
    An entry in this list represents a module implemented by the
    server, as per Section 5.6.5 of RFC 7950, with a particular
    set of supported features and deviations.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: Annotated[str, Field(alias='ietf-yang-library:namespace')]
    """
    The XML namespace identifier for this module.
    """
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Optional[str],
        Field(
            alias='ietf-yang-library:revision', pattern='^(?=^\\d{4}-\\d{2}-\\d{2}$).*$'
        ),
    ] = None
    """
    The YANG module or submodule revision date.  If no revision
    statement is present in the YANG module or submodule, this
    leaf is not instantiated.
    """
    location: Annotated[
        Optional[List[str]], Field(alias='ietf-yang-library:location')
    ] = []
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """
    submodule: Annotated[
        Optional[List[SubmoduleListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:submodule'),
    ]
    feature: Annotated[
        Optional[List[FeatureLeafList]],
        Field(default_factory=list, alias='ietf-yang-library:feature'),
    ]
    """
    List of all YANG feature names from this module that are
    supported by the server, regardless whether they are defined
    in the module or any included submodule.
    """
    deviation: Annotated[
        Optional[List[DeviationLeafList]],
        Field(default_factory=list, alias='ietf-yang-library:deviation'),
    ]
    """
    List of all YANG deviation modules used by this server to
    modify the conformance of the module associated with this
    entry.  Note that the same module can be used for deviations
    for multiple modules, so the same entry MAY appear within
    multiple 'module' entries.

    This reference MUST NOT (directly or indirectly)
    refer to the module being deviated.

    Robust clients may want to make sure that they handle a
    situation where a module deviates itself (directly or
    indirectly) gracefully.
    """


class ModuleListEntry2(BaseModel):
    """
    Each entry represents one revision of one module
    currently supported by the server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: Annotated[str, Field(alias='ietf-yang-library:namespace')]
    """
    The XML namespace identifier for this module.
    """
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[
        str,
        Field(
            alias='ietf-yang-library:name',
            pattern='^(?=^[a-zA-Z_][a-zA-Z0-9\\-_.]*$)(?=^.|..|[^xX].*|.[^mM].*|..[^lL].*$).*$',
        ),
    ]
    """
    The YANG module or submodule name.
    """
    revision: Annotated[
        Union[RevisionIdentifierType, RevisionLeaf51],
        Field(alias='ietf-yang-library:revision'),
    ]
    """
    The YANG module or submodule revision date.
    A zero-length string is used if no revision statement
    is present in the YANG module or submodule.
    """
    schema: Annotated[Optional[str], Field(alias='ietf-yang-library:schema')] = None
    """
    Contains a URL that represents the YANG schema
    resource for this module or submodule.

    This leaf will only be present if there is a URL
    available for retrieval of the schema for this entry.
    """
    feature: Annotated[
        Optional[List[FeatureLeafList2]],
        Field(default_factory=list, alias='ietf-yang-library:feature'),
    ]
    """
    List of YANG feature names from this module that are
    supported by the server, regardless of whether they are
    defined in the module or any included submodule.
    """
    deviation: Annotated[
        Optional[List[DeviationListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:deviation'),
    ]
    conformance_type: Annotated[
        ConformanceTypeLeaf, Field(alias='ietf-yang-library:conformance-type')
    ]
    submodule: Annotated[
        Optional[List[SubmoduleListEntry3]],
        Field(default_factory=list, alias='ietf-yang-library:submodule'),
    ]


class ModulesStateContainer(BaseModel):
    """
    Contains YANG module monitoring information.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    module_set_id: Annotated[str, Field(alias='ietf-yang-library:module-set-id')]
    """
    Contains a server-specific identifier representing
    the current set of modules and submodules.  The
    server MUST change the value of this leaf if the
    information represented by the 'module' list instances
    has changed.
    """
    module: Annotated[
        Optional[List[ModuleListEntry2]],
        Field(default_factory=list, alias='ietf-yang-library:module'),
    ]


class ModuleSetListEntry(BaseModel):
    """
    A set of modules that may be used by one or more schemas.

    A module set does not have to be referentially complete,
    i.e., it may define modules that contain import statements
    for other modules not included in the module set.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    name: Annotated[str, Field(alias='ietf-yang-library:name')]
    """
    An arbitrary name of the module set.
    """
    module: Annotated[
        Optional[List[ModuleListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:module'),
    ]
    import_only_module: Annotated[
        Optional[List[ImportOnlyModuleListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:import-only-module'),
    ]


class YangLibraryContainer(BaseModel):
    """
    Container holding the entire YANG library of this server.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    module_set: Annotated[
        Optional[List[ModuleSetListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:module-set'),
    ]
    schema: Annotated[
        Optional[List[SchemaListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:schema'),
    ]
    datastore: Annotated[
        Optional[List[DatastoreListEntry]],
        Field(default_factory=list, alias='ietf-yang-library:datastore'),
    ]
    content_id: Annotated[str, Field(alias='ietf-yang-library:content-id')]
    """
    A server-generated identifier of the contents of the
    '/yang-library' tree.  The server MUST change the value of
    this leaf if the information represented by the
    '/yang-library' tree, except '/yang-library/content-id', has
    changed.
    """


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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-yang-library'
    prefix: ClassVar[Optional[str]] = 'yanglib'
    yang_library: Annotated[
        Optional[YangLibraryContainer], Field(alias='ietf-yang-library:yang-library')
    ] = None
    modules_state: Annotated[
        Optional[ModulesStateContainer], Field(alias='ietf-yang-library:modules-state')
    ] = None
from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class StatisticsContainer(BaseModel):
    """
    A collection of interface-related statistics objects.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    discontinuity_time: Annotated[
        str,
        Field(
            alias='ietf-interfaces:discontinuity-time',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ]
    """
    The time on the most recent occasion at which any one or
    more of this interface's counters suffered a
    discontinuity.  If no such discontinuities have occurred
    since the last re-initialization of the local management
    subsystem, then this node contains the time the local
    management subsystem re-initialized itself.
    """
    in_octets: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-octets', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets received on the interface,
    including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_unicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-unicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were not addressed to a
    multicast or broadcast address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_broadcast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-broadcast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a broadcast
    address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_multicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-multicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a multicast
    address at this sub-layer.  For a MAC-layer protocol,
    this includes both Group and Functional addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_discards: Annotated[
        Optional[int], Field(alias='ietf-interfaces:in-discards', ge=0, le=4294967295)
    ] = None
    """
    The number of inbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being deliverable to a higher-layer
    protocol.  One possible reason for discarding such a
    packet could be to free up buffer space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_errors: Annotated[
        Optional[int], Field(alias='ietf-interfaces:in-errors', ge=0, le=4294967295)
    ] = None
    """
    For packet-oriented interfaces, the number of inbound
    packets that contained errors preventing them from being
    deliverable to a higher-layer protocol.  For character-
    oriented or fixed-length interfaces, the number of
    inbound transmission units that contained errors
    preventing them from being deliverable to a higher-layer
    protocol.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_unknown_protos: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-unknown-protos', ge=0, le=4294967295),
    ] = None
    """
    For packet-oriented interfaces, the number of packets
    received via the interface that were discarded because
    of an unknown or unsupported protocol.  For
    character-oriented or fixed-length interfaces that
    support protocol multiplexing, the number of
    transmission units received via the interface that were
    discarded because of an unknown or unsupported protocol.
    For any interface that does not support protocol
    multiplexing, this counter is not present.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_octets: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:out-octets', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets transmitted out of the
    interface, including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_unicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:out-unicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were not addressed
    to a multicast or broadcast address at this sub-layer,
    including those that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_broadcast_pkts: Annotated[
        Optional[int],
        Field(
            alias='ietf-interfaces:out-broadcast-pkts', ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were addressed to a
    broadcast address at this sub-layer, including those
    that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_multicast_pkts: Annotated[
        Optional[int],
        Field(
            alias='ietf-interfaces:out-multicast-pkts', ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were addressed to a
    multicast address at this sub-layer, including those
    that were discarded or not sent.  For a MAC-layer
    protocol, this includes both Group and Functional
    addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_discards: Annotated[
        Optional[int], Field(alias='ietf-interfaces:out-discards', ge=0, le=4294967295)
    ] = None
    """
    The number of outbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being transmitted.  One possible reason
    for discarding such a packet could be to free up buffer
    space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_errors: Annotated[
        Optional[int], Field(alias='ietf-interfaces:out-errors', ge=0, le=4294967295)
    ] = None
    """
    For packet-oriented interfaces, the number of outbound
    packets that could not be transmitted because of errors.
    For character-oriented or fixed-length interfaces, the
    number of outbound transmission units that could not be
    transmitted because of errors.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class StatisticsContainer2(BaseModel):
    """
    A collection of interface-related statistics objects.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    discontinuity_time: Annotated[
        str,
        Field(
            alias='ietf-interfaces:discontinuity-time',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ]
    """
    The time on the most recent occasion at which any one or
    more of this interface's counters suffered a
    discontinuity.  If no such discontinuities have occurred
    since the last re-initialization of the local management
    subsystem, then this node contains the time the local
    management subsystem re-initialized itself.
    """
    in_octets: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-octets', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets received on the interface,
    including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_unicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-unicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were not addressed to a
    multicast or broadcast address at this sub-layer.
    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_broadcast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-broadcast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a broadcast
    address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_multicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-multicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a multicast
    address at this sub-layer.  For a MAC-layer protocol,
    this includes both Group and Functional addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_discards: Annotated[
        Optional[int], Field(alias='ietf-interfaces:in-discards', ge=0, le=4294967295)
    ] = None
    """
    The number of inbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being deliverable to a higher-layer
    protocol.  One possible reason for discarding such a
    packet could be to free up buffer space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_errors: Annotated[
        Optional[int], Field(alias='ietf-interfaces:in-errors', ge=0, le=4294967295)
    ] = None
    """
    For packet-oriented interfaces, the number of inbound
    packets that contained errors preventing them from being
    deliverable to a higher-layer protocol.  For character-
    oriented or fixed-length interfaces, the number of
    inbound transmission units that contained errors
    preventing them from being deliverable to a higher-layer
    protocol.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    in_unknown_protos: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:in-unknown-protos', ge=0, le=4294967295),
    ] = None
    """
    For packet-oriented interfaces, the number of packets
    received via the interface that were discarded because
    of an unknown or unsupported protocol.  For
    character-oriented or fixed-length interfaces that
    support protocol multiplexing, the number of
    transmission units received via the interface that were
    discarded because of an unknown or unsupported protocol.
    For any interface that does not support protocol
    multiplexing, this counter is not present.
    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_octets: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:out-octets', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets transmitted out of the
    interface, including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_unicast_pkts: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:out-unicast-pkts', ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were not addressed
    to a multicast or broadcast address at this sub-layer,
    including those that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_broadcast_pkts: Annotated[
        Optional[int],
        Field(
            alias='ietf-interfaces:out-broadcast-pkts', ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were addressed to a
    broadcast address at this sub-layer, including those
    that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_multicast_pkts: Annotated[
        Optional[int],
        Field(
            alias='ietf-interfaces:out-multicast-pkts', ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted and that were addressed to a
    multicast address at this sub-layer, including those
    that were discarded or not sent.  For a MAC-layer
    protocol, this includes both Group and Functional
    addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_discards: Annotated[
        Optional[int], Field(alias='ietf-interfaces:out-discards', ge=0, le=4294967295)
    ] = None
    """
    The number of outbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being transmitted.  One possible reason
    for discarding such a packet could be to free up buffer
    space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """
    out_errors: Annotated[
        Optional[int], Field(alias='ietf-interfaces:out-errors', ge=0, le=4294967295)
    ] = None
    """
    For packet-oriented interfaces, the number of outbound
    packets that could not be transmitted because of errors.
    For character-oriented or fixed-length interfaces, the
    number of outbound transmission units that could not be
    transmitted because of errors.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class EnumerationEnum10(Enum):
    other = 'other'
    static = 'static'
    dynamic = 'dynamic'


class EnumerationEnum11(Enum):
    preferred = 'preferred'
    deprecated = 'deprecated'
    invalid = 'invalid'
    inaccessible = 'inaccessible'
    unknown = 'unknown'
    tentative = 'tentative'
    duplicate = 'duplicate'
    optimistic = 'optimistic'


class EnumerationEnum12(Enum):
    incomplete = 'incomplete'
    reachable = 'reachable'
    stale = 'stale'
    delay = 'delay'
    probe = 'probe'


class EnumerationEnum13(Enum):
    up = 'up'
    down = 'down'
    testing = 'testing'


class EnumerationEnum14(Enum):
    up = 'up'
    down = 'down'
    testing = 'testing'
    unknown = 'unknown'
    dormant = 'dormant'
    not_present = 'not-present'
    lower_layer_down = 'lower-layer-down'


class EnumerationEnum15(Enum):
    preferred = 'preferred'
    deprecated = 'deprecated'
    invalid = 'invalid'
    inaccessible = 'inaccessible'
    unknown = 'unknown'
    tentative = 'tentative'
    duplicate = 'duplicate'
    optimistic = 'optimistic'


class EnumerationEnum16(Enum):
    incomplete = 'incomplete'
    reachable = 'reachable'
    stale = 'stale'
    delay = 'delay'
    probe = 'probe'


class EnumerationEnum6(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class EnumerationEnum7(Enum):
    up = 'up'
    down = 'down'
    testing = 'testing'


class EnumerationEnum8(Enum):
    up = 'up'
    down = 'down'
    testing = 'testing'
    unknown = 'unknown'
    dormant = 'dormant'
    not_present = 'not-present'
    lower_layer_down = 'lower-layer-down'


class EnumerationEnum9(Enum):
    other = 'other'
    static = 'static'
    dhcp = 'dhcp'
    link_layer = 'link-layer'
    random = 'random'


class AdminStatusLeaf(RootModel[EnumerationEnum7]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum7
    """
    The desired state of the interface.

    This leaf has the same read semantics as ifAdminStatus.
    """


class AdminStatusLeaf2(RootModel[EnumerationEnum13]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum13
    """
    The desired state of the interface.

    This leaf has the same read semantics as ifAdminStatus.
    """


class AutoconfContainer(BaseModel):
    """
    Parameters to control the autoconfiguration of IPv6
    addresses, as described in RFC 4862.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    create_global_addresses: Annotated[
        Optional[bool], Field(alias='ietf-ip:create-global-addresses')
    ] = True
    """
    If enabled, the host creates global addresses as
    described in RFC 4862.
    """
    create_temporary_addresses: Annotated[
        Optional[bool], Field(alias='ietf-ip:create-temporary-addresses')
    ] = False
    """
    If enabled, the host creates temporary addresses as
    described in RFC 4941.
    """
    temporary_valid_lifetime: Annotated[
        Optional[int],
        Field(alias='ietf-ip:temporary-valid-lifetime', ge=0, le=4294967295),
    ] = 604800
    """
    The time period during which the temporary address
    is valid.
    """
    temporary_preferred_lifetime: Annotated[
        Optional[int],
        Field(alias='ietf-ip:temporary-preferred-lifetime', ge=0, le=4294967295),
    ] = 86400
    """
    The time period during which the temporary address is
    preferred.
    """


class IpAddressOriginType(RootModel[EnumerationEnum9]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum9
    """
    The origin of an address.
    """


class LinkUpDownTrapEnableLeaf(RootModel[EnumerationEnum6]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum6
    """
    Controls whether linkUp/linkDown SNMP notifications
    should be generated for this interface.

    If this node is not configured, the value 'enabled' is
    operationally used by the server for interfaces that do
    not operate on top of any other interface (i.e., there are
    no 'lower-layer-if' entries), and 'disabled' otherwise.
    """


class NeighborOriginType(RootModel[EnumerationEnum10]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum10
    """
    The origin of a neighbor entry.
    """


class NetmaskCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    netmask: Annotated[
        Optional[str],
        Field(
            alias='ietf-ip:netmask',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$',
        ),
    ] = None
    """
    The subnet specified as a netmask.
    """


class NetmaskCase2(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    netmask: Annotated[
        Optional[str],
        Field(
            alias='ietf-ip:netmask',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$',
        ),
    ] = None
    """
    The subnet specified as a netmask.
    """


class OperStatusLeaf(RootModel[EnumerationEnum8]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum8
    """
    The current operational state of the interface.

    This leaf has the same semantics as ifOperStatus.
    """


class OperStatusLeaf2(RootModel[EnumerationEnum14]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum14
    """
    The current operational state of the interface.

    This leaf has the same semantics as ifOperStatus.
    """


class OriginLeaf(RootModel[IpAddressOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: IpAddressOriginType
    """
    The origin of this address.
    """


class OriginLeaf2(RootModel[NeighborOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: NeighborOriginType
    """
    The origin of this neighbor entry.
    """


class OriginLeaf3(RootModel[IpAddressOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: IpAddressOriginType
    """
    The origin of this address.
    """


class OriginLeaf4(RootModel[NeighborOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: NeighborOriginType
    """
    The origin of this neighbor entry.
    """


class OriginLeaf5(RootModel[IpAddressOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: IpAddressOriginType
    """
    The origin of this address.
    """


class OriginLeaf6(RootModel[NeighborOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: NeighborOriginType
    """
    The origin of this neighbor entry.
    """


class OriginLeaf7(RootModel[IpAddressOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: IpAddressOriginType
    """
    The origin of this address.
    """


class OriginLeaf8(RootModel[NeighborOriginType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: NeighborOriginType
    """
    The origin of this neighbor entry.
    """


class PrefixLengthCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    prefix_length: Annotated[
        Optional[int], Field(alias='ietf-ip:prefix-length', ge=0, le=32)
    ] = None
    """
    The length of the subnet prefix.
    """


class PrefixLengthCase2(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    prefix_length: Annotated[
        Optional[int], Field(alias='ietf-ip:prefix-length', ge=0, le=32)
    ] = None
    """
    The length of the subnet prefix.
    """


class StateLeaf(RootModel[EnumerationEnum12]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum12
    """
    The Neighbor Unreachability Detection state of this
    entry.
    """


class StateLeaf2(RootModel[EnumerationEnum16]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum16
    """
    The Neighbor Unreachability Detection state of this
    entry.
    """


class StatusLeaf(RootModel[EnumerationEnum11]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum11
    """
    The status of an address.  Most of the states correspond
    to states from the IPv6 Stateless Address
    Autoconfiguration protocol.
    """


class StatusLeaf2(RootModel[EnumerationEnum15]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum15
    """
    The status of an address.  Most of the states correspond
    to states from the IPv6 Stateless Address
    Autoconfiguration protocol.
    """


class NeighborListEntry(BaseModel):
    """
    A list of mappings from IPv4 addresses to
    link-layer addresses.

    Entries in this list in the intended configuration are
    used as static entries in the ARP Cache.

    In the operational state, this list represents the ARP
    Cache.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\d\\w]+)?$).*$',
        ),
    ]
    """
    The IPv4 address of the neighbor node.
    """
    link_layer_address: Annotated[
        str,
        Field(
            alias='ietf-ip:link-layer-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ]
    """
    The link-layer address of the neighbor node.
    """
    origin: Annotated[Optional[OriginLeaf2], Field(alias='ietf-ip:origin')] = None


class NeighborListEntry2(BaseModel):
    """
    A list of mappings from IPv6 addresses to
    link-layer addresses.

    Entries in this list in the intended configuration are
    used as static entries in the Neighbor Cache.

    In the operational state, this list represents the
    Neighbor Cache.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\d\\w]+)?$)(?=^(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?$).*$',
        ),
    ]
    """
    The IPv6 address of the neighbor node.
    """
    link_layer_address: Annotated[
        str,
        Field(
            alias='ietf-ip:link-layer-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ]
    """
    The link-layer address of the neighbor node.

    In the operational state, if the neighbor's 'state' leaf
    is 'incomplete', this leaf is not instantiated.
    """
    origin: Annotated[Optional[OriginLeaf4], Field(alias='ietf-ip:origin')] = None
    is_router: Annotated[
        Optional[List[None]],
        Field(alias='ietf-ip:is-router', max_length=1, min_length=1),
    ] = None
    """
    Indicates that the neighbor node acts as a router.
    """
    state: Annotated[Optional[StateLeaf], Field(alias='ietf-ip:state')] = None


class NeighborListEntry3(BaseModel):
    """
    A list of mappings from IPv4 addresses to
    link-layer addresses.

    This list represents the ARP Cache.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\d\\w]+)?$).*$',
        ),
    ]
    """
    The IPv4 address of the neighbor node.
    """
    link_layer_address: Annotated[
        Optional[str],
        Field(
            alias='ietf-ip:link-layer-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ] = None
    """
    The link-layer address of the neighbor node.
    """
    origin: Annotated[Optional[OriginLeaf6], Field(alias='ietf-ip:origin')] = None


class NeighborListEntry4(BaseModel):
    """
    A list of mappings from IPv6 addresses to
    link-layer addresses.

    This list represents the Neighbor Cache.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\d\\w]+)?$)(?=^(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?$).*$',
        ),
    ]
    """
    The IPv6 address of the neighbor node.
    """
    link_layer_address: Annotated[
        Optional[str],
        Field(
            alias='ietf-ip:link-layer-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ] = None
    """
    The link-layer address of the neighbor node.
    """
    origin: Annotated[Optional[OriginLeaf8], Field(alias='ietf-ip:origin')] = None
    is_router: Annotated[
        Optional[List[None]],
        Field(alias='ietf-ip:is-router', max_length=1, min_length=1),
    ] = None
    """
    Indicates that the neighbor node acts as a router.
    """
    state: Annotated[Optional[StateLeaf2], Field(alias='ietf-ip:state')] = None


class AddressListEntry(BaseModel):
    """
    The list of IPv4 addresses on the interface.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\d\\w]+)?$).*$',
        ),
    ]
    """
    The IPv4 address on the interface.
    """
    subnet: Annotated[
        Union[PrefixLengthCase, NetmaskCase], Field(alias='ietf-ip:subnet')
    ]
    origin: Annotated[Optional[OriginLeaf], Field(alias='ietf-ip:origin')] = None


class AddressListEntry2(BaseModel):
    """
    The list of IPv6 addresses on the interface.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\d\\w]+)?$)(?=^(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?$).*$',
        ),
    ]
    """
    The IPv6 address on the interface.
    """
    prefix_length: Annotated[int, Field(alias='ietf-ip:prefix-length', ge=0, le=128)]
    """
    The length of the subnet prefix.
    """
    origin: Annotated[Optional[OriginLeaf3], Field(alias='ietf-ip:origin')] = None
    status: Annotated[Optional[StatusLeaf], Field(alias='ietf-ip:status')] = None


class AddressListEntry3(BaseModel):
    """
    The list of IPv4 addresses on the interface.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\d\\w]+)?$).*$',
        ),
    ]
    """
    The IPv4 address on the interface.
    """
    subnet: Annotated[
        Optional[Union[PrefixLengthCase2, NetmaskCase2]], Field(alias='ietf-ip:subnet')
    ] = None
    origin: Annotated[Optional[OriginLeaf5], Field(alias='ietf-ip:origin')] = None


class AddressListEntry4(BaseModel):
    """
    The list of IPv6 addresses on the interface.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    ip: Annotated[
        str,
        Field(
            alias='ietf-ip:ip',
            pattern='^(?=^((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\d\\w]+)?$)(?=^(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?$).*$',
        ),
    ]
    """
    The IPv6 address on the interface.
    """
    prefix_length: Annotated[int, Field(alias='ietf-ip:prefix-length', ge=0, le=128)]
    """
    The length of the subnet prefix.
    """
    origin: Annotated[Optional[OriginLeaf7], Field(alias='ietf-ip:origin')] = None
    status: Annotated[Optional[StatusLeaf2], Field(alias='ietf-ip:status')] = None


class Ipv4Container(BaseModel):
    """
    Parameters for the IPv4 address family.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    enabled: Annotated[Optional[bool], Field(alias='ietf-ip:enabled')] = True
    """
    Controls whether IPv4 is enabled or disabled on this
    interface.  When IPv4 is enabled, this interface is
    connected to an IPv4 stack, and the interface can send
    and receive IPv4 packets.
    """
    forwarding: Annotated[Optional[bool], Field(alias='ietf-ip:forwarding')] = False
    """
    Controls IPv4 packet forwarding of datagrams received by,
    but not addressed to, this interface.  IPv4 routers
    forward datagrams.  IPv4 hosts do not (except those
    source-routed via the host).
    """
    mtu: Annotated[Optional[int], Field(alias='ietf-ip:mtu', ge=68, le=65535)] = None
    """
    The size, in octets, of the largest IPv4 packet that the
    interface will send and receive.

    The server may restrict the allowed values for this leaf,
    depending on the interface's type.

    If this leaf is not configured, the operationally used MTU
    depends on the interface's type.
    """
    address: Annotated[
        Optional[List[AddressListEntry]],
        Field(default_factory=list, alias='ietf-ip:address'),
    ]
    neighbor: Annotated[
        Optional[List[NeighborListEntry]],
        Field(default_factory=list, alias='ietf-ip:neighbor'),
    ]
    bind_ni_name: Annotated[
        Optional[str], Field(alias='ietf-network-instance:bind-ni-name')
    ] = None
    """
    Network instance to which IPv4 interface is bound.
    """


class Ipv4Container2(BaseModel):
    """
    Interface-specific parameters for the IPv4 address family.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    forwarding: Annotated[Optional[bool], Field(alias='ietf-ip:forwarding')] = None
    """
    Indicates whether IPv4 packet forwarding is enabled or
    disabled on this interface.
    """
    mtu: Annotated[Optional[int], Field(alias='ietf-ip:mtu', ge=68, le=65535)] = None
    """
    The size, in octets, of the largest IPv4 packet that the
    interface will send and receive.
    """
    address: Annotated[
        Optional[List[AddressListEntry3]],
        Field(default_factory=list, alias='ietf-ip:address'),
    ]
    neighbor: Annotated[
        Optional[List[NeighborListEntry3]],
        Field(default_factory=list, alias='ietf-ip:neighbor'),
    ]


class Ipv6Container(BaseModel):
    """
    Parameters for the IPv6 address family.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    enabled: Annotated[Optional[bool], Field(alias='ietf-ip:enabled')] = True
    """
    Controls whether IPv6 is enabled or disabled on this
    interface.  When IPv6 is enabled, this interface is
    connected to an IPv6 stack, and the interface can send
    and receive IPv6 packets.
    """
    forwarding: Annotated[Optional[bool], Field(alias='ietf-ip:forwarding')] = False
    """
    Controls IPv6 packet forwarding of datagrams received by,
    but not addressed to, this interface.  IPv6 routers
    forward datagrams.  IPv6 hosts do not (except those
    source-routed via the host).
    """
    mtu: Annotated[
        Optional[int], Field(alias='ietf-ip:mtu', ge=1280, le=4294967295)
    ] = None
    """
    The size, in octets, of the largest IPv6 packet that the
    interface will send and receive.

    The server may restrict the allowed values for this leaf,
    depending on the interface's type.

    If this leaf is not configured, the operationally used MTU
    depends on the interface's type.
    """
    address: Annotated[
        Optional[List[AddressListEntry2]],
        Field(default_factory=list, alias='ietf-ip:address'),
    ]
    neighbor: Annotated[
        Optional[List[NeighborListEntry2]],
        Field(default_factory=list, alias='ietf-ip:neighbor'),
    ]
    dup_addr_detect_transmits: Annotated[
        Optional[int],
        Field(alias='ietf-ip:dup-addr-detect-transmits', ge=0, le=4294967295),
    ] = 1
    """
    The number of consecutive Neighbor Solicitation messages
    sent while performing Duplicate Address Detection on a
    tentative address.  A value of zero indicates that
    Duplicate Address Detection is not performed on
    tentative addresses.  A value of one indicates a single
    transmission with no follow-up retransmissions.
    """
    autoconf: Annotated[
        Optional[AutoconfContainer], Field(alias='ietf-ip:autoconf')
    ] = None
    bind_ni_name: Annotated[
        Optional[str], Field(alias='ietf-network-instance:bind-ni-name')
    ] = None
    """
    Network instance to which IPv6 interface is bound.
    """


class Ipv6Container2(BaseModel):
    """
    Parameters for the IPv6 address family.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-ip'
    prefix: ClassVar[Optional[str]] = 'ip'
    forwarding: Annotated[Optional[bool], Field(alias='ietf-ip:forwarding')] = False
    """
    Indicates whether IPv6 packet forwarding is enabled or
    disabled on this interface.
    """
    mtu: Annotated[
        Optional[int], Field(alias='ietf-ip:mtu', ge=1280, le=4294967295)
    ] = None
    """
    The size, in octets, of the largest IPv6 packet that the
    interface will send and receive.
    """
    address: Annotated[
        Optional[List[AddressListEntry4]],
        Field(default_factory=list, alias='ietf-ip:address'),
    ]
    neighbor: Annotated[
        Optional[List[NeighborListEntry4]],
        Field(default_factory=list, alias='ietf-ip:neighbor'),
    ]


class InterfaceListEntry(BaseModel):
    """
    The list of interfaces on the device.

    The status of an interface is available in this list in the
    operational state.  If the configuration of a
    system-controlled interface cannot be used by the system
    (e.g., the interface hardware present does not match the
    interface type), then the configuration is not applied to
    the system-controlled interface shown in the operational
    state.  If the configuration of a user-controlled interface
    cannot be used by the system, the configured interface is
    not instantiated in the operational state.

    System-controlled interfaces created by the system are
    always present in this list in the operational state,
    whether or not they are configured.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    name: Annotated[str, Field(alias='ietf-interfaces:name')]
    """
    The name of the interface.

    A device MAY restrict the allowed values for this leaf,
    possibly depending on the type of the interface.
    For system-controlled interfaces, this leaf is the
    device-specific name of the interface.

    If a client tries to create configuration for a
    system-controlled interface that is not present in the
    operational state, the server MAY reject the request if
    the implementation does not support pre-provisioning of
    interfaces or if the name refers to an interface that can
    never exist in the system.  A Network Configuration
    Protocol (NETCONF) server MUST reply with an rpc-error
    with the error-tag 'invalid-value' in this case.

    If the device supports pre-provisioning of interface
    configuration, the 'pre-provisioning' feature is
    advertised.

    If the device allows arbitrarily named user-controlled
    interfaces, the 'arbitrary-names' feature is advertised.

    When a configured user-controlled interface is created by
    the system, it is instantiated with the same name in the
    operational state.

    A server implementation MAY map this leaf to the ifName
    MIB object.  Such an implementation needs to use some
    mechanism to handle the differences in size and characters
    allowed between this leaf and ifName.  The definition of
    such a mechanism is outside the scope of this document.
    """
    description: Annotated[
        Optional[str], Field(alias='ietf-interfaces:description')
    ] = None
    """
    A textual description of the interface.

    A server implementation MAY map this leaf to the ifAlias
    MIB object.  Such an implementation needs to use some
    mechanism to handle the differences in size and characters
    allowed between this leaf and ifAlias.  The definition of
    such a mechanism is outside the scope of this document.

    Since ifAlias is defined to be stored in non-volatile
    storage, the MIB implementation MUST map ifAlias to the
    value of 'description' in the persistently stored
    configuration.
    """
    type: Annotated[str, Field(alias='ietf-interfaces:type')]
    """
    The type of the interface.

    When an interface entry is created, a server MAY
    initialize the type leaf with a valid value, e.g., if it
    is possible to derive the type from the name of the
    interface.

    If a client tries to set the type of an interface to a
    value that can never be used by the system, e.g., if the
    type is not supported or if the type does not match the
    name of the interface, the server MUST reject the request.
    A NETCONF server MUST reply with an rpc-error with the
    error-tag 'invalid-value' in this case.
    """
    enabled: Annotated[Optional[bool], Field(alias='ietf-interfaces:enabled')] = True
    """
    This leaf contains the configured, desired state of the
    interface.

    Systems that implement the IF-MIB use the value of this
    leaf in the intended configuration to set
    IF-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry
    has been initialized, as described in RFC 2863.

    Changes in this leaf in the intended configuration are
    reflected in ifAdminStatus.
    """
    link_up_down_trap_enable: Annotated[
        Optional[LinkUpDownTrapEnableLeaf],
        Field(alias='ietf-interfaces:link-up-down-trap-enable'),
    ] = None
    admin_status: Annotated[
        AdminStatusLeaf, Field(alias='ietf-interfaces:admin-status')
    ]
    oper_status: Annotated[OperStatusLeaf, Field(alias='ietf-interfaces:oper-status')]
    last_change: Annotated[
        Optional[str],
        Field(
            alias='ietf-interfaces:last-change',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ] = None
    """
    The time the interface entered its current operational
    state.  If the current state was entered prior to the
    last re-initialization of the local network management
    subsystem, then this node is not present.
    """
    if_index: Annotated[
        int, Field(alias='ietf-interfaces:if-index', ge=1, le=2147483647)
    ]
    """
    The ifIndex value for the ifEntry represented by this
    interface.
    """
    phys_address: Annotated[
        Optional[str],
        Field(
            alias='ietf-interfaces:phys-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ] = None
    """
    The interface's address at its protocol sub-layer.  For
    example, for an 802.x interface, this object normally
    contains a Media Access Control (MAC) address.  The
    interface's media-specific modules must define the bit
    and byte ordering and the format of the value of this
    object.  For interfaces that do not have such an address
    (e.g., a serial line), this node is not present.
    """
    higher_layer_if: Annotated[
        Optional[List[str]], Field(alias='ietf-interfaces:higher-layer-if')
    ] = []
    """
    A list of references to interfaces layered on top of this
    interface.
    """
    lower_layer_if: Annotated[
        Optional[List[str]], Field(alias='ietf-interfaces:lower-layer-if')
    ] = []
    """
    A list of references to interfaces layered underneath this
    interface.
    """
    speed: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:speed', ge=0, le=18446744073709551615),
    ] = None
    """
    An estimate of the interface's current bandwidth in bits
    per second.  For interfaces that do not vary in
    bandwidth or for those where no accurate estimation can
    be made, this node should contain the nominal bandwidth.
    For interfaces that have no concept of bandwidth, this
    node is not present.
    """
    statistics: Annotated[
        Optional[StatisticsContainer], Field(alias='ietf-interfaces:statistics')
    ] = None
    ipv4: Annotated[Optional[Ipv4Container], Field(alias='ietf-ip:ipv4')] = None
    ipv6: Annotated[Optional[Ipv6Container], Field(alias='ietf-ip:ipv6')] = None
    bind_ni_name: Annotated[
        Optional[str], Field(alias='ietf-network-instance:bind-ni-name')
    ] = None
    """
    Network instance to which an interface is bound.
    """


class InterfaceListEntry2(BaseModel):
    """
    The list of interfaces on the device.

    System-controlled interfaces created by the system are
    always present in this list, whether or not they are
    configured.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    name: Annotated[str, Field(alias='ietf-interfaces:name')]
    """
    The name of the interface.

    A server implementation MAY map this leaf to the ifName
    MIB object.  Such an implementation needs to use some
    mechanism to handle the differences in size and characters
    allowed between this leaf and ifName.  The definition of
    such a mechanism is outside the scope of this document.
    """
    type: Annotated[str, Field(alias='ietf-interfaces:type')]
    """
    The type of the interface.
    """
    admin_status: Annotated[
        AdminStatusLeaf2, Field(alias='ietf-interfaces:admin-status')
    ]
    oper_status: Annotated[OperStatusLeaf2, Field(alias='ietf-interfaces:oper-status')]
    last_change: Annotated[
        Optional[str],
        Field(
            alias='ietf-interfaces:last-change',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ] = None
    """
    The time the interface entered its current operational
    state.  If the current state was entered prior to the
    last re-initialization of the local network management
    subsystem, then this node is not present.
    """
    if_index: Annotated[
        int, Field(alias='ietf-interfaces:if-index', ge=1, le=2147483647)
    ]
    """
    The ifIndex value for the ifEntry represented by this
    interface.
    """
    phys_address: Annotated[
        Optional[str],
        Field(
            alias='ietf-interfaces:phys-address',
            pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$',
        ),
    ] = None
    """
    The interface's address at its protocol sub-layer.  For
    example, for an 802.x interface, this object normally
    contains a Media Access Control (MAC) address.  The
    interface's media-specific modules must define the bit
    and byte ordering and the format of the value of this
    object.  For interfaces that do not have such an address
    (e.g., a serial line), this node is not present.
    """
    higher_layer_if: Annotated[
        Optional[List[str]], Field(alias='ietf-interfaces:higher-layer-if')
    ] = []
    """
    A list of references to interfaces layered on top of this
    interface.
    """
    lower_layer_if: Annotated[
        Optional[List[str]], Field(alias='ietf-interfaces:lower-layer-if')
    ] = []
    """
    A list of references to interfaces layered underneath this
    interface.
    """
    speed: Annotated[
        Optional[int],
        Field(alias='ietf-interfaces:speed', ge=0, le=18446744073709551615),
    ] = None
    """
    An estimate of the interface's current bandwidth in bits
    per second.  For interfaces that do not vary in
    bandwidth or for those where no accurate estimation can

    be made, this node should contain the nominal bandwidth.
    For interfaces that have no concept of bandwidth, this
    node is not present.
    """
    statistics: Annotated[
        Optional[StatisticsContainer2], Field(alias='ietf-interfaces:statistics')
    ] = None
    ipv4: Annotated[Optional[Ipv4Container2], Field(alias='ietf-ip:ipv4')] = None
    ipv6: Annotated[Optional[Ipv6Container2], Field(alias='ietf-ip:ipv6')] = None


class InterfacesStateContainer(BaseModel):
    """
    Data nodes for the operational state of interfaces.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    interface: Annotated[
        Optional[List[InterfaceListEntry2]],
        Field(default_factory=list, alias='ietf-interfaces:interface'),
    ]


class InterfacesContainer(BaseModel):
    """
    Interface parameters.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    interface: Annotated[
        Optional[List[InterfaceListEntry]],
        Field(default_factory=list, alias='ietf-interfaces:interface'),
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
    namespace: ClassVar[Optional[str]] = 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
    prefix: ClassVar[Optional[str]] = 'if'
    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias='ietf-interfaces:interfaces')
    ] = None
    interfaces_state: Annotated[
        Optional[InterfacesStateContainer],
        Field(alias='ietf-interfaces:interfaces-state'),
    ] = None
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


class StreamListEntry2(BaseModel):
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


class StreamsContainer2(BaseModel):
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
        Optional[List[StreamListEntry2]],
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
        Optional[StreamsContainer2], Field(alias='ietf-restconf-monitoring:streams')
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
from __future__ import annotations

from typing import Annotated, ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field


class NotificationContainer(BaseModel):
    """
    internal struct to start a notification
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        'urn:ietf:params:xml:ns:netconf:notification:1.0'
    )
    prefix: ClassVar[Optional[str]] = 'ncEvent'
    event_time: Annotated[
        str,
        Field(
            alias='notifications:eventTime',
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$',
        ),
    ]
    """
    The date-and-time type is a profile of the ISO 8601
    standard for representation of dates and times using the
    Gregorian calendar.  The profile is defined by the
    date-time production in Section 5.6 of RFC 3339.

    The date-and-time type is compatible with the dateTime XML
    schema type with the following notable exceptions:

    (a) The date-and-time type does not allow negative years.

    (b) The date-and-time time-offset -00:00 indicates an unknown
        time zone (see RFC 3339) while -00:00 and +00:00 and Z
        all represent the same time zone in dateTime.

    (c) The canonical format (see below) of data-and-time values
        differs from the canonical format used by the dateTime XML
        schema type, which requires all times to be in UTC using
        the time-offset 'Z'.

    This type is not equivalent to the DateAndTime textual
    convention of the SMIv2 since RFC 3339 uses a different
    separator between full-date and full-time and provides
    higher resolution of time-secfrac.

    The canonical format for date-and-time values with a known time
    zone uses a numeric time zone offset that is calculated using
    the device's configured known offset to UTC time.  A change of
    the device's offset to UTC time will cause date-and-time values
    to change accordingly.  Such changes might happen periodically
    in case a server follows automatically daylight saving time
    (DST) time zone offset changes.  The canonical format for
    date-and-time values with an unknown time zone (usually
    referring to the notion of local time) uses the time-offset
    -00:00.
    """


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
        'urn:ietf:params:xml:ns:netconf:notification:1.0'
    )
    prefix: ClassVar[Optional[str]] = 'ncEvent'
    notification: Annotated[
        Optional[NotificationContainer], Field(alias='notifications:notification')
    ] = None
from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IntervalListEntry(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:cesnet:libnetconf2-netconf-server'
    prefix: ClassVar[Optional[str]] = 'np2'
    anchor: Annotated[
        str,
        Field(
            alias='libnetconf2-netconf-server:anchor',
            pattern='^(?=^(1[0-2]|[1-9])m|[1-4]w|[1-7]d|(2[0-4]|1[0-9]|[1-9])h$).*$',
        ),
    ]
    """
    The time anchor for the notification. The anchor is the time
    before the certificate expiration when a notification will be sent.
    It is essentially the lower bound of the given interval.
    """
    period: Annotated[
        str,
        Field(
            alias='libnetconf2-netconf-server:period',
            pattern='^(?=^(1[0-2]|[1-9])m|[1-4]w|[1-7]d|(2[0-4]|1[0-9]|[1-9])h$).*$',
        ),
    ]
    """
    The period of the notification. The period is the time
    between two notifications within the given time interval.
    """


class CertificateExpirationNotifIntervalsContainer(BaseModel):
    """
    Container for the certificate expiration notification intervals. Its child nodes describe the ability to set
    the time intervals for the certificate expiration notifications. These intervals are given in the form of an
    anchor and a period. By default, these notifications are generated 3, 2, and 1 month; 2 weeks; 7, 6, 5, 4, 3,
    2 and 1 day before a certificate expires. Additionally, notifications are generated on the day of expiration
    and every day thereafter.

    Simplified example of YANG data that describe the default intervals:

    Anchor         Period
      3m     ...     1m
      2w     ...     1w
      7d     ...     1d
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:cesnet:libnetconf2-netconf-server'
    prefix: ClassVar[Optional[str]] = 'np2'
    interval: Annotated[
        Optional[List[IntervalListEntry]],
        Field(default_factory=list, alias='libnetconf2-netconf-server:interval'),
    ]


class Ln2NetconfServerContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = 'urn:cesnet:libnetconf2-netconf-server'
    prefix: ClassVar[Optional[str]] = 'np2'
    certificate_expiration_notif_intervals: Annotated[
        Optional[CertificateExpirationNotifIntervalsContainer],
        Field(
            alias='libnetconf2-netconf-server:certificate-expiration-notif-intervals'
        ),
    ] = None
    ignored_hello_module: Annotated[
        Optional[List[str]],
        Field(alias='libnetconf2-netconf-server:ignored-hello-module'),
    ] = []
    """
    List of implemented sysrepo YANG modules that will not be reported the NETCONF server in its <hello> messages.
    """


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
    namespace: ClassVar[Optional[str]] = 'urn:cesnet:libnetconf2-netconf-server'
    prefix: ClassVar[Optional[str]] = 'np2'
    ln2_netconf_server: Annotated[
        Optional[Ln2NetconfServerContainer],
        Field(alias='libnetconf2-netconf-server:ln2-netconf-server'),
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