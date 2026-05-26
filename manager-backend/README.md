# Manager Backend

## Overview

Python/FastAPI application that communicates with network devices via NETCONF. Handles YANG schema processing, datastore reading, and configuration editing.

## Tech Stack

- **Python 3.14+**
- **FastAPI** – REST API framework
- **ncclient** – NETCONF client library
- **yangson** – YANG schema processing
- **pyang** – YANG module validation
- **wireup** – Dependency Injection
- **Pydantic** – data validation and models
- **pytest** – testing

## Project Structure

```
manager-backend/
├── app/
│   ├── core/               # Application configuration
│   ├── routers/
│   │   ├── connection_router.py   # NETCONF connection endpoints
│   │   ├── datastore_router.py    # Datastore CRUD endpoints
│   │   └── module_router.py       # YANG module endpoints
│   ├── services/
│   │   ├── datastore_service.py   # Datastore business logic
│   │   └── module_service.py      # Module download, schema processing
│   ├── resources/          # Downloaded YANG modules
│   ├── dependencies.py     # DI container, ConnectionManager
│   ├── models.py           # Pydantic models (Connection, SchemaNode, etc.)
│   └── main.py             # FastAPI application entry point
├── tests/
│   ├── test_connection.py
│   ├── test_datastores.py
│   ├── test_modules.py
│   └── conftest.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /connect` | Establish NETCONF connection |
| `POST /disconnect` | Close connection |
| `GET /modules` | List YANG modules |
| `GET /modules/{name}/schema` | Get module schema |
| `GET /datastores/{store}/{module}` | Get datastore content |
| `POST /datastores/{store}/edit` | Edit configuration |
| `GET /datastores/{store}/staged` | Get staged changes |

## Running

### Docker

```sh
docker compose up -d
```

Available on port `8000`.

### Local Development

```sh
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### Tests

```sh
uv run pytest
```

## Models

- **Connection** – NETCONF connection details (host, port, user, password)
- **DataStore** – datastore type enum (startup, candidate, running)
- **SchemaNode** – YANG schema tree node (kind, config, description, children)
- **EditConfigRequest** – edit request (module_name, path, value)
- **ModuleSummary** – module summary (name, status, revision)
