# Architecture

This document describes the architecture of ApiForge, a modern Python API client generator.

## Overview

ApiForge is a config-driven API client library designed for transport-level abstraction. It defines API endpoints declaratively in JSON and provides a typed client with automatic validation, retry logic, and extensible adapters.

**Primary use case**: Transport core for MCP (Model Context Protocol) servers.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Code                            │
├─────────────────────────────────────────────────────────────┤
│                       Client                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Config    │  │  Resources  │  │      Executor       │ │
│  │   Loader    │  │   Manager   │  │    (Coordinator)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Adapter Layer                            │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ BaseAdapter │  │ RequestsAdapter │  │  Custom Adapters │ │
│  │   (ABC)     │  │   (requests)    │  │   (httpx, etc)  │ │
│  │ + hook      │  │                 │  │                 │ │
│  └─────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Response Layer                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                      Response                           ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ││
│  │  │  json() │  │  text() │  │   data  │  │   ok    │  ││
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Package Structure

```
apiforge/
├── __init__.py              # Public API with backward-compat aliases
├── client.py                # Client (main entry point)
├── executor.py              # Executor (coordinates adapter calls)
├── resource.py              # Resource (endpoint definition)
├── response.py              # Response (HTTP response wrapper)
├── exceptions.py            # Exception hierarchy
├── cli.py                   # CLI tools
├── config/                  # Configuration package
│   ├── __init__.py          # Re-exports
│   ├── loader.py            # load_config()
│   ├── validator.py         # JSON Schema validation
│   └── discovery.py         # get_config_path(), list_configs()
├── adapters/                # Transport layer
│   ├── __init__.py
│   ├── base.py              # BaseAdapter (ABC) with on_before_request
│   └── requests_adapter.py  # RequestsAdapter (requests library)
├── core/                    # Backward-compat shims (do not modify)
└── serializers/             # Unused (dead code)
```

## Core Components

### Client

**File:** `apiforge/client.py`

Main entry point. Responsibilities:
- Load and validate configuration
- Manage resources (API endpoints)
- Coordinate request execution
- Provide convenience methods (get, post, put, delete, patch)
- Support `on_before_request` hook for MCP integration

```python
class Client:
    def __init__(self, config_path=None, config=None, 
                 on_before_request=None, ...):
        # Load config
        # Create adapter with hook
        # Create executor
        # Load resources
    
    def request(self, resource_name, params=None, data=None, **kwargs):
        # Get resource
        # Validate params
        # Execute via executor
```

### Executor

**File:** `apiforge/executor.py`

Coordinates HTTP execution. Responsibilities:
- Manage adapter lifecycle
- Delegate to adapter for all HTTP operations
- Handle adapter creation if not provided

```python
class Executor:
    def execute(self, method, path, params=None, data=None, headers=None):
        # Delegate to adapter
```

### BaseAdapter / RequestsAdapter

**Files:** `apiforge/adapters/base.py`, `apiforge/adapters/requests_adapter.py`

Transport layer. Responsibilities:
- Send HTTP requests
- Handle retries with backoff
- Process HTTP errors (401, 404, 429, 5xx)
- Support `on_before_request` hook

```python
class BaseAdapter(ABC):
    def __init__(self, on_before_request=None):
        self._on_before_request = on_before_request
    
    @abstractmethod
    def request(self, method, url, ...):
        pass

class RequestsAdapter(BaseAdapter):
    def request(self, method, url, ...):
        if self._on_before_request:
            self._on_before_request(method, url)
        # Execute with retries
```

### Resource

**File:** `apiforge/resource.py`

API endpoint definition. Responsibilities:
- Store endpoint metadata (path, method, parameters)
- Validate required parameters
- Build URLs with path parameters
- Validate HTTP method

```python
class Resource:
    VALID_METHODS = frozenset({"GET", "POST", "PUT", "DELETE", "PATCH"})
    
    def __init__(self, name, path, method="GET", ...):
        if method.upper() not in self.VALID_METHODS:
            raise ValueError(f"Invalid method '{method}'")
```

### Response

**File:** `apiforge/response.py`

HTTP response wrapper. Responsibilities:
- Store response data (status, content, headers)
- Provide lazy parsing (json, text)
- Handle encoding fallback (UTF-8 → latin-1)

```python
class Response:
    def text(self):
        try:
            return self.content.decode("utf-8")
        except UnicodeDecodeError:
            return self.content.decode("latin-1")
```

### Config Package

**Directory:** `apiforge/config/`

Configuration handling. Split into three modules:
- `loader.py`: Read JSON files
- `validator.py`: JSON Schema validation
- `discovery.py`: Find installed configs

## Data Flow

### Request Lifecycle

```
1. User calls client.request("resource_name", params={...})
   ↓
2. Client looks up Resource by name
   ↓
3. Resource validates required parameters
   ↓
4. Client calls executor.execute(method, path, params, data, headers)
   ↓
5. Executor delegates to adapter.request(method, url, params, data, headers)
   ↓
6. Adapter calls on_before_request hook (if set)
   ↓
7. Adapter builds full URL, merges headers
   ↓
8. Adapter sends HTTP request with retries
   ↓
9. Adapter handles errors (401, 404, 429, 5xx)
   ↓
10. Adapter wraps response in Response
   ↓
11. Response returned to user
```

### Configuration Loading

```
1. User provides config_path or config dict
   ↓
2. load_config() reads JSON file
   ↓
3. Schema validation against api_template.json
   ↓
4. Detailed error messages if validation fails
   ↓
5. Config dict returned to client
   ↓
6. Client creates Resource objects from config["resources"]
```

## MCP Integration

### Access Control

```python
from apiforge import Client

def enforce_read_only(method: str, url: str):
    """MCP policy: only allow GET requests."""
    if method != "GET":
        raise PermissionError("Read-only mode")

client = Client(
    config_path="config.json",
    on_before_request=enforce_read_only
)
```

### Token Management

```python
def refresh_token_before_request(method: str, url: str):
    """MCP hook: ensure valid token."""
    token = token_manager.get_token()
    # Token is now valid

client = Client(
    config_path="config.json",
    on_before_request=refresh_token_before_request
)
```

## Design Patterns

- **Facade Pattern**: Client provides simple interface to complex subsystem
- **Strategy Pattern**: Adapters allow swapping transport implementations
- **Template Method Pattern**: Base classes define interface, subclasses implement
- **Hook Pattern**: on_before_request for MCP policy enforcement

## Error Handling

### Immediate Failures
- 401 Unauthorized → `ApiForgeAuthenticationError`
- 404 Not Found → `ApiForgeResourceNotFoundError`
- 4xx Client Errors → `ApiForgeRequestError`

### Retryable Failures
- 429 Rate Limited → Retry after `Retry-After` header
- 5xx Server Errors → Retry with linear backoff
- Connection/Timeout errors → Retry with linear backoff

## Testing

### Test Coverage

- 250 tests across 11 test files
- Unit tests for all core components
- Integration tests for end-to-end flows
- Config validation tests for Yandex APIs

```
tests/
├── test_adapter.py       # Adapter, Executor tests
├── test_client.py        # Client, Resource, Response tests
├── test_config.py        # Config loading, validation tests
├── test_cli.py           # CLI tests
├── test_serializers.py   # Serializer tests
├── test_integration.py   # End-to-end tests
└── test_yandex_*.py      # Yandex config tests (5 files)
```

## Future Enhancements

1. **Async Support**: `AsyncAdapter` using httpx
2. **Caching**: Response caching layer
3. **Rate Limiting**: Client-side rate limiting
4. **Logging**: Request/response logging
5. **Metrics**: Performance metrics collection
