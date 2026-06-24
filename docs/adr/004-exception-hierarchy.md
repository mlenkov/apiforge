# ADR-004: Exception Hierarchy Design

## Status

Accepted

## Context

The library needs to handle various error conditions:

1. Configuration errors (invalid JSON, missing fields)
2. Validation errors (missing required parameters)
3. HTTP errors (401, 404, 429, 5xx)
4. Network errors (connection, timeout)
5. Processing errors (invalid JSON response)

Users need to handle these errors programmatically.

## Decision

We will implement a **hierarchical exception system**:

```
ApiForgeError (base)
├── ApiForgeConfigError
├── ApiForgeValidationError
└── ApiForgeRequestError
    ├── ApiForgeAuthenticationError
    ├── ApiForgeRateLimitError
    └── ApiForgeResourceNotFoundError
```

### Exception Classes

```python
class ApiForgeError(Exception):
    """Base exception for all ApiForge errors."""
    def __init__(self, message, response=None, data=None):
        self.message = message
        self.response = response
        self.data = data

class ApiForgeRequestError(ApiForgeError):
    """HTTP request errors."""
    def __init__(self, message, status_code=None, response=None, data=None):
        self.status_code = status_code

class ApiForgeAuthenticationError(ApiForgeRequestError):
    """401 Unauthorized errors."""
    pass

class ApiForgeRateLimitError(ApiForgeRequestError):
    """429 Rate Limited errors."""
    def __init__(self, message, retry_after=None, ...):
        self.retry_after = retry_after

class ApiForgeResourceNotFoundError(ApiForgeRequestError):
    """404 Not Found errors."""
    pass

class ApiForgeConfigError(ApiForgeError):
    """Configuration errors."""
    pass

class ApiForgeValidationError(ApiForgeError):
    """Validation errors."""
    def __init__(self, message, errors=None, ...):
        self.errors = errors or {}
```

## Alternatives Considered

### Option 1: Single Exception Class

Use one exception class for all errors:

```python
class ApiForgeError(Exception):
    def __init__(self, message, error_type=None, status_code=None, ...):
        self.error_type = error_type
        self.status_code = status_code
```

**Pros:**
- Simple implementation
- Easy to catch all errors

**Cons:**
- Hard to handle specific errors
- No type safety
- Poor IDE support

### Option 2: Use Built-in Exceptions

Raise standard Python exceptions:

```python
raise ValueError("Invalid configuration")
raise ConnectionError("Failed to connect")
```

**Pros:**
- Familiar to Python developers
- No custom exceptions needed

**Cons:**
- No domain-specific semantics
- Hard to distinguish from other errors
- No additional context (response, retry_after)

### Option 3: Flat Exception Structure

All exceptions inherit from base:

```python
class ApiForgeError(Exception): pass
class ApiForgeConfigError(ApiForgeError): pass
class ApiForgeRequestError(ApiForgeError): pass
class ApiForgeAuthError(ApiForgeError): pass
class ApiForgeRateLimitError(ApiForgeError): pass
```

**Pros:**
- Simple hierarchy
- Easy to catch specific errors

**Cons:**
- No grouping of related errors
- Can't catch "all request errors" easily

## Consequences

### Positive

1. **Granular Handling**: Catch specific error types
2. **Rich Context**: Each exception carries relevant data
3. **Clear Semantics**: Error names describe the problem
4. **IDE Support**: Autocomplete for exception types
5. **Backward Compatible**: Can add new exceptions without breaking

### Negative

1. **More Classes**: More code to maintain
2. **Learning Curve**: Users must learn exception hierarchy
3. **Overhead**: Small performance cost for exception creation

### Mitigations

1. **Documentation**: Clear documentation of exception hierarchy
2. **Examples**: Show common error handling patterns
3. **Base Class**: `ApiForgeError` catches all library errors

## Usage Examples

### Catch All Errors

```python
try:
    client.request("users")
except ApiForgeError as e:
    print(f"ApiForge error: {e}")
```

### Catch Request Errors

```python
try:
    client.request("users")
except ApiForgeRequestError as e:
    print(f"Request failed: {e.status_code}")
```

### Catch Specific Errors

```python
try:
    client.request("users")
except ApiForgeAuthenticationError:
    print("Please check your API credentials")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ApiForgeResourceNotFoundError:
    print("Resource not found")
```

### Handle Configuration Errors

```python
try:
    client = ApiForgeClient(config_path="config.json")
except ApiForgeConfigError as e:
    print(f"Invalid configuration: {e}")
```

## Implementation Details

### Exception Attributes

| Exception | Attributes |
|-----------|------------|
| `ApiForgeError` | `message`, `response`, `data` |
| `ApiForgeRequestError` | + `status_code` |
| `ApiForgeRateLimitError` | + `retry_after` |
| `ApiForgeValidationError` | + `errors` |

### Response Object

The `response` attribute contains the raw HTTP response (if available):

```python
except ApiForgeRequestError as e:
    if e.response:
        print(f"Response headers: {e.response.headers}")
```

## References

- Python Exception Handling: https://docs.python.org/3/tutorial/errors.html
- requests Exceptions: https://docs.python-requests.org/en/latest/api/#exceptions
