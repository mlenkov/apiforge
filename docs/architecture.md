# Architecture

This document describes the architecture of ApiForge, a modern Python API client generator.

## Overview

ApiForge is designed as a config-driven API client library. Instead of hand-coding API endpoints, you define them declaratively in a JSON file, and the library dynamically builds a typed client from that config.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Code                            │
├─────────────────────────────────────────────────────────────┤
│                      ApiForgeClient                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Config    │  │  Resources  │  │      Executor       │ │
│  │   Loader    │  │   Manager   │  │    (Coordinator)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Adapter Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ BaseAdapter │  │ HTTPAdapter │  │   Custom Adapters   │ │
│  │   (ABC)     │  │ (requests)  │  │    (httpx, etc)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Serialization Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │BaseSerializer│ │JSONSerializer│ │  Custom Serializers  │ │
│  │    (ABC)    │  │   (json)    │  │   (msgpack, etc)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Response Layer                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   ApiForgeResponse                      ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ││
│  │  │  json() │  │  text() │  │   data  │  │   ok    │  ││
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### ApiForgeClient

**File:** `apiforge/core/client.py`

The main entry point for users. Responsibilities:

- Load and validate configuration
- Manage resources (API endpoints)
- Coordinate request execution
- Provide convenience methods (get, post, put, delete, patch)

```python
class ApiForgeClient:
    def __init__(self, config_path=None, config=None, ...):
        # Load config
        # Create adapter
        # Create executor
        # Load resources
    
    def request(self, resource_name, params=None, data=None, **kwargs):
        # Get resource
        # Validate params
        # Build URL
        # Execute via executor
```

### ApiForgeExecutor

**File:** `apiforge/core/executor.py`

A coordinator that delegates HTTP transport to adapters. Responsibilities:

- Manage adapter lifecycle
- Provide clean interface for client
- Handle adapter creation if not provided

```python
class ApiForgeExecutor:
    def __init__(self, adapter=None, ...):
        # Store adapter or create default
    
    def execute(self, method, path, params=None, data=None, headers=None):
        # Delegate to adapter
```

### BaseAdapter / HTTPAdapter

**Files:** `apiforge/adapters/base.py`, `apiforge/adapters/http.py`

The transport layer. Responsibilities:

- Send HTTP requests
- Handle retries with backoff
- Process HTTP errors (401, 404, 429, 5xx)
- Manage connections

```python
class BaseAdapter(ABC):
    @abstractmethod
    def request(self, method, url, params=None, data=None, headers=None):
        pass
    
    def get(self, url, params=None, headers=None):
        return self.request("GET", url, params=params, headers=headers)
    # ... other convenience methods

class HTTPAdapter(BaseAdapter):
    def request(self, method, url, params=None, data=None, headers=None):
        # Build URL
        # Merge headers
        # Execute with retries
        # Handle errors
        # Return ApiForgeResponse
```

### Resource

**File:** `apiforge/core/resource.py`

Represents an API endpoint definition. Responsibilities:

- Store endpoint metadata (path, method, parameters)
- Validate required parameters
- Build URLs with path parameters

```python
class Resource:
    def __init__(self, name, path, method="GET", parameters=None, ...):
        # Store metadata
    
    def validate_params(self, params):
        # Check required params
        return missing_params
    
    def build_url(self, base_url, **kwargs):
        # Format path with kwargs
        # Return full URL
```

### ApiForgeResponse

**File:** `apiforge/core/response.py`

Wraps HTTP responses. Responsibilities:

- Store response data (status, content, headers)
- Provide lazy parsing (json, text)
- Indicate success/failure

```python
class ApiForgeResponse:
    def __init__(self, status_code, content, headers):
        self.status_code = status_code
        self.content = content
        self.headers = headers
    
    def json(self):
        return json.loads(self.content)
    
    def text(self):
        return self.content.decode("utf-8")
    
    @property
    def ok(self):
        return 200 <= self.status_code < 300
```

### Config Loader

**File:** `apiforge/config.py`

Handles configuration loading and validation. Responsibilities:

- Read JSON files
- Validate structure against schema
- Provide detailed error messages
- Discover installed configs

```python
def load_config(path):
    # Check file exists
    # Parse JSON
    # Validate against schema
    # Return config dict

def list_configs():
    # Scan ~/.apiforge/configs/
    # Return {provider: [apis]}
```

### Exceptions

**File:** `apiforge/exceptions.py`

Error hierarchy for structured error handling:

```
ApiForgeError (base)
├── ApiForgeConfigError
├── ApiForgeValidationError
└── ApiForgeRequestError
    ├── ApiForgeAuthenticationError
    ├── ApiForgeRateLimitError
    └── ApiForgeResourceNotFoundError
```

## Data Flow

### Request Lifecycle

```
1. User calls client.request("resource_name", params={...})
   ↓
2. Client looks up Resource by name
   ↓
3. Resource validates required parameters
   ↓
4. Resource builds URL with path parameters
   ↓
5. Client calls executor.execute(method, path, params, data, headers)
   ↓
6. Executor delegates to adapter.request(method, url, params, data, headers)
   ↓
7. Adapter builds full URL, merges headers
   ↓
8. Adapter sends HTTP request with retries
   ↓
9. Adapter handles errors (401, 404, 429, 5xx)
   ↓
10. Adapter wraps response in ApiForgeResponse
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

## Design Patterns

### Facade Pattern

`ApiForgeClient` provides a simple interface to the complex subsystem:

```python
# Simple interface
client = ApiForgeClient(config_path="config.json")
response = client.request("users")

# Hides: config loading, resource management, executor, adapter, retries
```

### Strategy Pattern

Adapters allow swapping transport implementations:

```python
# Use default HTTPAdapter
client = ApiForgeClient(config_path="config.json")

# Or inject custom adapter
client._adapter = MyCustomAdapter()
```

### Template Method Pattern

Base classes define the interface, subclasses provide implementation:

```python
class BaseAdapter(ABC):
    @abstractmethod
    def request(self, method, url, ...):  # Template
        pass

class HTTPAdapter(BaseAdapter):
    def request(self, method, url, ...):  # Implementation
        # requests-based implementation
```

### Builder Pattern

Resources are built from configuration:

```python
Resource(
    name="users",
    path="/users/{user_id}",
    method="GET",
    parameters={"user_id": {"type": "integer", "required": True}}
)
```

## Error Handling Strategy

### Immediate Failures

- **401 Unauthorized**: Raises `ApiForgeAuthenticationError` immediately
- **404 Not Found**: Raises `ApiForgeResourceNotFoundError` immediately
- **4xx Client Errors**: Raises `ApiForgeRequestError` immediately

### Retryable Failures

- **429 Rate Limited**: Retries after `Retry-After` header or delay
- **5xx Server Errors**: Retries with linear backoff
- **Connection Errors**: Retries with linear backoff
- **Timeouts**: Retries with linear backoff

### Retry Configuration

```python
adapter = HTTPAdapter(
    max_retries=3,      # Maximum retry attempts
    retry_delay=1.0,    # Base delay in seconds
)
```

Backoff formula: `delay * (attempt + 1)`

## Extensibility Points

### Custom Adapters

Implement `BaseAdapter` to use different HTTP libraries:

```python
class AsyncHTTPAdapter(BaseAdapter):
    async def request(self, method, url, ...):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, ...)
            return ApiForgeResponse(...)
```

### Custom Serializers

Implement `BaseSerializer` for different data formats:

```python
class MsgPackSerializer(BaseSerializer):
    def dumps(self, obj):
        return msgpack.packb(obj)
    
    def loads(self, data):
        return msgpack.unpackb(data)
```

### Custom Exception Handling

Catch specific exceptions for granular control:

```python
try:
    response = client.request("users")
except ApiForgeRateLimitError as e:
    time.sleep(e.retry_after)
    response = client.request("users")
```

## Performance Considerations

### Connection Pooling

`HTTPAdapter` uses `requests.Session` which provides connection pooling by default.

### Lazy Parsing

`ApiForgeResponse` parses JSON/text only when accessed:

```python
response = client.request("users")
# Response content is raw bytes

data = response.json()
# Now parsed
```

### Timeout Configuration

```python
client = ApiForgeClient(
    config_path="config.json",
    timeout=30.0,  # 30 second timeout
)
```

## Testing Strategy

### Unit Tests

- Test each component in isolation
- Mock HTTP responses
- Verify error handling

### Integration Tests

- Test complete request lifecycle
- Test configuration loading
- Test error propagation

### Test Coverage

Current coverage: 117 tests across 6 files

```
tests/
├── test_adapter.py      # HTTPAdapter, Executor
├── test_client.py       # Client, Resource, Response
├── test_config.py       # Config loading
├── test_cli.py          # CLI commands
├── test_serializers.py  # JSON serializer
└── test_integration.py  # End-to-end tests
```

## Future Architecture

### Planned Enhancements

1. **Async Support**: `AsyncHTTPAdapter` using httpx
2. **Caching**: Response caching layer
3. **Rate Limiting**: Client-side rate limiting
4. **Logging**: Request/response logging
5. **Metrics**: Performance metrics collection

### Architecture Evolution

The current architecture supports these enhancements through:

- **Adapter pattern**: Async adapter can be added without changing core
- **Strategy pattern**: Caching can be added as a decorator
- **Middleware pattern**: Logging/metrics can be added as middleware
