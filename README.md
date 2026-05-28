
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

The architecture consists of a backend, a frontend and an optional simulated network device.

### Backend

The backend is written in Python and exposes a FastAPI server that the frontend connects to.



The backend consists of NETCONF client


The system consists of the following parts:

network device: simulated or real hardware, exposes a NETCONF server
Backend: provides a restful fastapi server, around a NETCONF client
frontend: provides ui


The system provides:
1. **Reading** YANG datastores from a NETCONF server
2. **Displaying** the datastore schema in an easily navigable, tree-based format
3. **Editing** writable datastore elements with real-time candidate/running datastore management

### Built With


## Technologies

### Backend Technologies

| Technology | Purpose |
|---|---|
| **Python 3.14** | Server-side programming language |
| **FastAPI** | Async REST API framework with automatic OpenAPI schema generation |
| **ncclient** | NETCONF client library for communicating with network devices |
| **pyang** | YANG module parsing and schema extraction |
| **uv** | Fast Python package manager and project tool |

### Frontend Technologies

| Technology | Purpose |
|---|---|
| **TypeScript** | Type-safe client-side language |
| **React** | Component-based UI library |
| **Ant Design** | UI component framework |
| **TanStack Query** | Server state management (caching, mutations, invalidation) |
| **Orval** | Generates type-safe API hooks from OpenAPI schema |
| **Vite** | Development server and build tool |

### Development Tools

| Tool | Purpose |
|---|---|
| **Docker & Docker Compose** | Containerization for backend, frontend, and simulated device |
| **GitHub Actions** | CI pipeline for static analysis and integration tests |
| **Ruff** | Python linter and formatter |
| **Basedpyright** | Python type checker |
| **Biome** | TypeScript/React linter and formatter |
| **pre-commit** | Git hooks for code quality enforcement |

## Architecture

### Backend Architecture

```
manager-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models and enums
│   ├── dependencies.py      # Dependency injection (connection manager)
│   ├── core/
│   │   └── config.py        # Application configuration
│   ├── auth/                # Authentication middleware
│   ├── routers/             # API endpoint definitions
│   │   ├── connection_router.py
│   │   ├── datastore_router.py
│   │   └── module_router.py
│   ├── services/            # Business logic layer
│   │   ├── datastore_service.py   # NETCONF datastore operations
│   │   └── module_service.py      # YANG module management
│   └── resources/           # Downloaded YANG modules storage
└── tests/                   # Integration tests (run against simulated device)
```

The backend follows a layered architecture:
- **Routers** — Thin controllers that handle HTTP concerns and delegate to services
- **Services** — Business logic: NETCONF operations, YANG parsing, XML↔JSON conversion
- **Models** — Shared data contracts (Pydantic BaseModel)

Key design decisions:
- YANG modules are parsed locally using `pyang` to extract schema trees
- NETCONF XML responses are converted to JSON for the frontend
- The connection manager maintains a single NETCONF session per server instance
- OpenAPI schema is auto-generated from FastAPI type annotations

### Frontend Architecture

```
manager-frontend/src/
├── api/                     # Generated API hooks (Orval)
│   ├── connection/
│   ├── datastore/
│   ├── modules/
│   └── model/               # Generated TypeScript types
├── components/
│   ├── connection/          # Device connection form
│   ├── datastore/           # Datastore panels, buttons, staged changes
│   ├── module/              # Module list, toolbar, content display
│   └── schema/              # YANG tree rendering, leaf editing
├── hooks/                   # Custom React hooks
├── utils/                   # Helper functions
└── App.tsx                  # Root layout with theme provider
```

Key design decisions:
- **End-to-end type safety**: FastAPI → OpenAPI schema → Orval → TypeScript hooks
- **No manual API calls**: All server communication uses generated TanStack Query hooks
- **Optimistic UI**: Mutations invalidate relevant queries automatically
- **Recursive tree rendering**: YANG schema displayed as nested collapsible panels

### API Design

The REST API follows resource-oriented design:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/connect` | Establish NETCONF session |
| `DELETE` | `/connect` | Disconnect |
| `GET` | `/modules/` | List available YANG modules |
| `POST` | `/modules/{name}/download` | Download module from device |
| `GET` | `/modules/{name}/schema` | Get parsed YANG schema tree |
| `GET` | `/datastore/{ds}/{module}/data` | Get datastore content as JSON |
| `PATCH` | `/datastore/{ds}` | Edit configuration (edit-config) |
| `POST` | `/datastore/{source}/copy-config/{target}` | Copy configuration |
| `POST` | `/datastore/{ds}/lock` | Lock datastore |
| `POST` | `/datastore/commit` | Commit candidate to running |

Mutations return `204 No Content` on success, `400` with error detail on failure.

## Getting Started

### Prerequisites

* Docker and Docker Compose
* Node.js 22+, Python 3.14+ and [uv](https://docs.astral.sh/uv/) for local development

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Peter-Vegvari/NETCONF-manager.git
   ```
2. Start both services (backend on :8000, frontend on :3000)
   ```sh
   cd manager-backend && docker compose up -d
   cd ../manager-frontend && docker compose up -d
   ```

### Local Development

**Backend:**
```sh
cd manager-backend
uv sync
uv run fastapi dev app/main.py
```

**Frontend:**
```sh
cd manager-frontend
npm install
npm run dev
```

**Regenerate API hooks** (after backend changes):
```sh
cd manager-frontend
npx orval
```

## Testing

The project uses a CI pipeline with GitHub Actions that runs on every push/PR to `main`:

**Backend:**
1. **Static analysis** — `ruff check`, `ruff format --check`, `basedpyright`
2. **Integration tests** — `pytest` running against a simulated NETCONF device ([netopeer2](https://github.com/CESNET/netopeer2)) via Docker Compose

**Frontend:**
1. **Static analysis** — `biome ci` (linting + formatting)

Run tests locally:
```sh
# Backend
cd manager-backend
docker compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from manager-backend

# Frontend
cd manager-frontend
npx @biomejs/biome ci .
```

## Roadmap

- [x] NETCONF connection management
- [x] Multi-device support
- [x] YANG datastore display with recursive schema tree
- [x] Editing writable datastore elements
- [x] Candidate datastore with commit/copy/lock operations
- [x] Staged changes diff view
- [x] CI pipeline with integration tests on simulated device
- [ ] Support multiple users at once

## License

Distributed under the MIT License. See `LICENSE` for more information.


https://en.wikipedia.org/wiki/YANG
