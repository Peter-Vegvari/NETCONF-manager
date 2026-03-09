from __future__ import annotations

from typing import Annotated, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportedAlgorithmsContainer(BaseModel):
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
        Optional[SupportedAlgorithmsContainer],
        Field(alias='iana-ssh-encryption-algs:supported-algorithms'),
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