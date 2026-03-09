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