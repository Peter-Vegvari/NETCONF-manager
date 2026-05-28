
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

The Network Configuration Protocol (NETCONF) is a network management protocol developed and standardized by the IETF. NETCONF provides mechanisms to install, manipulate, and delete the configuration of network devices.

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
1. pyang: library for validating, transforming YANG and code generator
2. yangson: library for working with configuration and state data modelled using YANG
3. ncclient: library for NETCONF client, that is used to establishes and maintain a persistent NETCONF session with a device


The HTTP API is written in FastAPI, it couldn't be truly RESTful, because NETCONF uses stateful RPC sessions.
The HTTP API has 3 routes, /connection, /module and /datastore

#### Connection

Manages the NETCONF session lifecycle.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/connect` | Get connection status |
| `POST` | `/connect` | Establish a new NETCONF session |
| `DELETE` | `/connect` | Close the active session |

#### Module

Before any Every module's YANG schema must be downloaded to the backend.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/modules/` | List all modules |
| `GET` | `/modules/{name}/schema` | Get parsed YANG schema tree |
| `POST` | `/modules/download-all` | Download every module's YANG schema to the backend |
| `POST` | `/modules/{name}/download` | Download a single module's YANG schema |
| `DELETE` | `/modules/{name}` | Delete a module's YANG schema locally |
| `DELETE` | `/modules/` | Delete all the modules's YANG schemas |

#### Datastore

Step to get the configuration for a datastore's module:
1.
2.
3.


| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/datastore/{ds}/{module}/data` | Get module data as JSON |
| `GET` | `/datastore/{ds}/{module}/data/{path}` | Get data at path |
| `GET` | `/datastore/{ds}/lock` | Get lock status |
| `GET` | `/datastore/staged/{module}` | Diff between running and candidate datastore config |
| `POST` | `/datastore/{source}/copy-config/{target}` | Copy one datastore config to another |
| `POST` | `/datastore/commit` | Commit candidate datastore config to running datastore config |
| `POST` | `/datastore/{ds}/lock` | Lock datastore |
| `PATCH` | `/datastore/{ds}` | Edit datastore config |
| `DELETE` | `/datastore/{ds}` | Delete datastore config |
| `DELETE` | `/datastore/{ds}/lock` | Unlock datastore |


The compose file for development is available at `manager-backend/docker-compose.override.yml`.
To rebuild and start the FastAPI server at `localhost:8000` and notconf at `localhost:830`, run these commands from the project rook:
```bash
cd manager-backend
sudo docker compose up --build -V -d
```



### Frontend

React


## Roadmap

- [x] NETCONF connection management
- [x] Multi-device support
- [x] YANG datastore display with recursive schema tree
- [x] Editing writable datastore elements
- [x] Candidate datastore with commit/copy/lock operations
- [x] CI pipeline with integration tests on simulated device
- [ ] Support multiple users at once

## License

Distributed under the MIT License. See `LICENSE` for more information.
