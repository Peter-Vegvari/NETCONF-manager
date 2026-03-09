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