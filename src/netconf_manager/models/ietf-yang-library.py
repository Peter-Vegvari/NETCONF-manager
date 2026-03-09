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


class EnumerationEnum(Enum):
    implement = 'implement'
    import_ = 'import'


class ConformanceTypeLeaf(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum
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