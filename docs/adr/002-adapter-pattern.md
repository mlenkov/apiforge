# ADR-002: Adapter Pattern for HTTP Transport

## Status

Accepted

## Context

We need to support HTTP requests to REST APIs. The library should:

1. Work with the popular `requests` library by default
2. Allow users to use alternative HTTP libraries (httpx, aiohttp, etc.)
3. Support both sync and async requests
4. Be testable without making real HTTP requests

## Decision

We will use the **Adapter Pattern** to abstract HTTP transport:

```python
class BaseAdapter(ABC):
    @abstractmethod
    def request(self, method, url, params=None, data=None, headers=None):
        pass

class HTTPAdapter(BaseAdapter):
    def request(self, method, url, params=None, data=None, headers=None):
        # Implementation using requests library
```

### Key Design Decisions

1. **Abstract Base Class**: `BaseAdapter` defines the interface
2. **Default Implementation**: `HTTPAdapter` uses `requests.Session`
3. **Dependency Injection**: Client accepts custom adapters
4. **Lazy Creation**: Adapter created on first use if not provided

## Alternatives Considered

### Option 1: Direct Requests Usage

Use `requests` directly in the client:

```python
class ApiForgeClient:
    def request(self, ...):
        response = requests.request(method, url, ...)
```

**Pros:**
- Simple implementation
- No abstraction overhead

**Cons:**
- Hard to swap HTTP libraries
- Difficult to test
- No support for async

### Option 2: Protocol-Based

Use Python protocols instead of ABC:

```python
class HTTPAdapter(Protocol):
    def request(self, method, url, ...) -> ApiForgeResponse: ...
```

**Pros:**
- More flexible (structural subtyping)
- No inheritance required

**Cons:**
- Less explicit interface
- Harder to document
- No default implementations

### Option 3: Middleware Pattern

Chain middleware for HTTP processing:

```python
client = ApiForgeClient(
    middleware=[RetryMiddleware(), LoggingMiddleware()]
)
```

**Pros:**
- Very flexible
- Composable

**Cons:**
- More complex
- Harder to understand
- Overkill for most use cases

## Consequences

### Positive

1. **Flexibility**: Users can swap HTTP libraries
2. **Testability**: Easy to mock for testing
3. **Extensibility**: Can add async support later
4. **Separation of Concerns**: Transport separate from business logic

### Negative

1. **Abstraction Overhead**: One more layer to understand
2. **Interface Contract**: Must maintain backward compatibility
3. **Documentation**: Need to document extension points

### Mitigations

1. **Clear Documentation**: Document adapter interface
2. **Default Implementation**: HTTPAdapter works out of the box
3. **Examples**: Provide examples of custom adapters

## Implementation Details

### HTTPAdapter Features

- Connection pooling via `requests.Session`
- Retry logic with exponential backoff
- Error handling (401, 404, 429, 5xx)
- Context manager support

### Custom Adapter Requirements

1. Implement `request()` method
2. Return `ApiForgeResponse` object
3. Handle errors appropriately
4. Support context manager (optional)

## References

- Adapter Pattern: https://en.wikipedia.org/wiki/Adapter_pattern
- requests Library: https://docs.python-requests.org/
- httpx Library: https://www.python-httpx.org/
