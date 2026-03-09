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