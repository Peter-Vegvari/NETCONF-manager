
<br />
<div align="center">
  <h3 align="center">NETCONF/YANG Browser</h3>
  <p align="center">
    Full-stack web application for managing network devices
  </p>
</div>


## Introduction

This application was developed as part of my project lab assignment at the Budapest University of Technology and Economics during my internship at Ericsson.

The goal was to create a vendor-agnostic, containerized full-stack web application capable of managing any network device that supports the NETCONF protocol.

## Technologies

### YANG

YANG is a data modeling language that provides a standardized way to model the configuration and state data of network elements, enabling network automation. It is developed and maintained by the Internet Engineering Task Force. YANG is a modular language and represents data structures in a hierarchical tree format. It includes numerous built-in data types, with the capability for users to derive additional application-specific types.

On actual network devices, YANG modules are usually augmented with vendor specific fields and functionality.

YANG instance data are stored in configuration datastores:
  | Configuration datastore | Description |
  |---|---|
  | `startup` | Contains instance data loaded at device start |
  | `running` | Contains instance data that is currently active on the device |
  | `candidate` | Contains temporary instance data that can be commited to the running configuration datastore |

Example of a YANG module:
```yang
module example - interfaces {
    namespace "urn:example:interfaces";
container interfaces {
        list interface {
            key "name";
            leaf name {
                type string;
            }
            leaf enabled {
                type boolean;
                default "true";
            }
        }
    }
}
```

Example of an instance data:
```xml
<interfaces xmlns=“urn:example:interfaces">
    <interface>
        <name>GigabitEthernet0/0/0</name>
        <enabled>true</enabled>
    </interface>
</interfaces>
```

### NETCONF

The Network Configuration Protocol (NETCONF) is a network management protocol developed and standardized by the IETF. NETCONF provides mechanisms to install, manipulate, and delete the configuration of network devices. NETCONF uses port 830.

Possible operations:
  | Operation | Description |
  |---|---|
  | `<get>` | Retrieve running configuration and device state information |
  | `<get-config>` | Retrieve all or part of a specified configuration datastore |
  | `<edit-config>` | Edit a configuration datastore by creating, deleting, merging or replacing content |
  | `<copy-config>` | Copy an entire configuration datastore to another configuration datastore |
  | `<delete-config>` | Delete a configuration datastore |
  | `<lock>` | Lock an entire configuration datastore of a device |
  | `<unlock>` | Release a configuration datastore lock previously obtained with the `<lock>` operation |
  | `<close-session>` | Request graceful termination of a NETCONF session |
  | `<kill-session>` | Force the termination of a NETCONF session |


Example of an operation where we request the instance data from the running configuration datastore:
```xml
<get-config>
      <source>
         <running/>
      </source>
      <filter>
         <interfaces xmlns="urn:example:interfaces"/>
      </filter>
</getconfig>
```

The reply is the instance data:
```xml
<interfaces xmlns=“urn:example:interfaces">
    <interface>
        <name>GigabitEthernet0/0/0</name>
        <enabled>true</enabled>
    </interface>
</interfaces>
```

## Architecture

The architecture consists of these 3 main parts:
1. A simulated NETCONF-capable device
2. A HTTP API written in FastAPI, wired to a NETCONF client
3. A React TypeScript GUI

### Simulated device

For the device simulation notconf, a NETCONF device simulator, is used. It is run in a container from a pre-built image published by notconf.

The device's startup configurations are to be placed at `manager-backend/tests/resources/yang-modules/startup`.

### Backend

The choice of language for the backend is Python, because of the preexisting tooling available for network development:
1. **pyang**: library for validating, transforming YANG and code generator
2. **yangson**: library for working with configuration and state data modelled using YANG
3. **ncclient**: library for NETCONF client, that is used to establishes and maintain a persistent NETCONF session with a device
4. **yanglint**: converts XML instance data to JSON using YANG modules.

Additional libraries used during development:
1. **uv**: for package and project management
2. **basedpyright**: for static analysis
3. **ruff**: for linting and formatting

The HTTP API is written in FastAPI, it couldn't be truly RESTful, because NETCONF uses stateful RPC sessions.

The application entry point is `app/main.py`, which creates the FastAPI app, registers middleware and routers, and writes the OpenAPI schema to the shared volume on startup.

Configuration is managed through `app/core/config.py` using pydantic-settings, reading environment variables for CORS origins, paths, and environment mode.

#### Connection

To avoid performance loss, it was necessary that the NETCONF session is reused between requests, making the HTTP API stateful.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/connect` | Get connection status |
| `POST` | `/connect` | Establish a new NETCONF session |
| `DELETE` | `/connect` | Close the active session |

#### Module

The schemas for the YANG modules are downloaded from the device to the backend filesystem. They are need for:
- Generating the schema tree via yangson
- Converting XML instance data to JSON viat yanglint
- Extracting namespace and revision metadata via pyang

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/modules/` | List all modules |
| `GET` | `/modules/{name}/schema` | Get parsed YANG schema tree |
| `POST` | `/modules/download-all` | Download every module's YANG schema to the backend |
| `POST` | `/modules/{name}/download` | Download a single module's YANG schema |
| `DELETE` | `/modules/{name}` | Delete a module's YANG schema locally |
| `DELETE` | `/modules/` | Delete all the modules's YANG schemas |

Example for a route:
```python
@module_router.get(
    "/{module_name}/schema", operation_id="getSchema", response_model_exclude_none=True # ensures null values are not sent
)
async def get_module_schema(module_name: str) -> SchemaNode:
    if not module_service.is_local(module_name):
        raise HTTPException(404, "Module not downloaded")
    return module_service.get_module_schema(module_name)
```

The schema output is a recursive tree of `SchemaNode` objects. Each node can contain:
- `kind`: container, list, leaf, leaf-list
- `description`: description that is defined in the YANG module
- `mandatory`: whether a value is required
- `config`: whether the node is read-only
- `type`: type for leaf nodes (string, int, etc...)
- `children`: child SchemaNodes

The truncated result of GET for ietf-interfaces
```json
{
  "children": {
    "ietf-interfaces:interfaces": {
      "kind": "container",
      "description": "Interface parameters.",
      "children": {
        "interface": {
          "kind": "list",
          "description": "The list of interfaces on the device...",
          "children": {
            "name": {
              "kind": "leaf",
              "description": "The name of the interface....",
              "mandatory": true,
              "type": {
                "base": "string"
              }
            },
            "description": {
              "kind": "leaf",
              "description": "A textual description of the interface...",
              "type": {
                "base": "string"
              }
            }
          }
        }
      }
    }
  }
}
```

#### Datastore

Every module's YANG schema should be downloaded first to the backend, before doing module specific requests. Otherwise the data from the network device will not be parsed correctly.

The data retrieval flow is:
1. Backend sends a `<get-config>` RPC with a subtree filter to the device
2. The device returns XML instance data
3. Backend writes the XML to a temp file and calls `yanglint` with the relevant YANG modules
4. `yanglint` outputs JSON, which is returned

For edit operations, the backend constructs an XML `<config>` element from the path and value, then sends it via `<edit-config>` RPC.

The staged diff endpoint compares the running and candidate datastores using `jsondiff` and returns the differences as a JSON patch.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/datastore/{ds}/{module}/data` | Get module data as JSON |
| `GET` | `/datastore/{ds}/{module}/data/{path}` | Get data at path |
| `GET` | `/datastore/{ds}/lock` | Get lock status |
| `GET` | `/datastore/staged/{module}` | Diff between running and candidate datastore config |
| `POST` | `/datastore/{source}/copy-config/{target}` | Copy one datastore config to another |
| `POST` | `/datastore/commit` | Commit candidate datastore config to running datastore config |
| `POST` | `/datastore/{ds}/lock` | Lock datastore |
| `PATCH` | `/datastore/{ds}/{module}/{path}` | Edit datastore config, value as string in body |
| `DELETE` | `/datastore/{ds}` | Delete datastore config |
| `DELETE` | `/datastore/{ds}/lock` | Unlock datastore |


The compose file for development is available at `manager-backend/docker-compose.override.yml`.
To rebuild and start the FastAPI server at `localhost:8000` and notconf at `localhost:830`, run these commands from the project rook:

```bash
cd manager-backend
sudo docker compose up --build -V -d
```

### Frontend

The frontend is a single-page application built in React and TypeScript, using Vite as the build tool:
1. **Ant Design**: UI component library, chosen for its simple yet elegant look.
2. **TanStack React Query**: server state management with automatic caching, background refetching, and devtools. Configured with a 30-second stale time
3. **Orval**: generates typed fetch functions and React Query hooks from the backend's OpenAPI schema. Also generates MSW mock handlers for testing
4. **Vite**: local development server
6. **react-cookie**: to persist site theme across sessions
7. **biomejs**: linting, formatting

To display all the

#### API client

The API client is fully generated by Orval from the OpenAPI schema from the backend. It watches the openapi.json and on changes will automatically generate a new API client in `src/api/`.

To display network configuration of a device in a meaningful way, both the schema and the instance data for a module must be queried by the API client:
```typescript
//manager-frontend/src/components/module/ModuleContent.tsx
const { data: schemaRes, isLoading: schemaLoading } = useGetSchema(
	module.name,
	{ query: { enabled: isLocal } },
);
const { data: dataRes, isLoading: dataLoading } = useGetModuleData(
	dataStore,
	module.name,
	{ query: { enabled: isLocal } },
);
```

and to to construct a combined React element:
```typescript
//manager-frontend/src/components/module/ModuleContent.tsx
		<SchemaTree
			node={schemaRes.data}
			data={dataRes?.status === 200 ? dataRes.data : undefined}
			dataStore={dataStore}
			moduleName={module.name}
		/>
```

Modifying the data is only possible on non read-only leaf nodes. After editing a value, it's query must be invalidated, to be refetched by the API client :
```typescript
//manager-frontend/src/components/schema/EditableValue.tsx
	const mutation = useEditConfig({
		mutation: {
			onSuccess: () => {
				queryClient.invalidateQueries({
					queryKey: getGetModuleDataQueryKey(dataStore, moduleName),
				});
				message.success("Configuration updated");
				setEditing(false);
			},
			onError: (err) => {
				message.error(`Edit failed: ${err}`);
			},
		},
	});
```


## Roadmap

- [x] NETCONF connection management
- [x] Multi-device support
- [x] YANG datastore display with recursive schema tree
- [x] Editing writable datastore elements
- [x] Candidate datastore with commit/copy/lock operations
- [x] CI pipeline with integration tests on simulated device
- [ ] Support multiple users at once
- [ ] E2E tests
- [ ] Mobile view

## License

Distributed under the MIT License. See `LICENSE` for more information.
