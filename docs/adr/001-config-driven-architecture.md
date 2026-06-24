# ADR-001: Config-Driven Architecture

## Status

Accepted

## Context

We need to build a Python API client library that can work with multiple REST APIs. The library should be:

1. Easy to use for common cases
2. Flexible enough for custom APIs
3. Maintainable as we add more API support
4. Type-safe where possible

## Decision

We will use a **config-driven architecture** where API endpoints are defined declaratively in JSON configuration files, and the library dynamically builds a typed client from that config.

### Configuration Structure

```json
{
  "base_url": "https://api.example.com",
  "auth": { "token": "..." },
  "resources": {
    "endpoint_name": {
      "path": "/path/{param}",
      "method": "GET",
      "parameters": { ... }
    }
  }
}
```

### Client Usage

```python
client = ApiForgeClient(config_path="config.json")
response = client.request("endpoint_name", params={...})
```

## Alternatives Considered

### Option 1: Code Generation

Generate Python code from API specs (OpenAPI, etc.)

**Pros:**
- Full IDE support
- Type checking at development time

**Cons:**
- Requires code generation step
- Harder to support dynamic APIs
- More complex build process

### Option 2: Decorator-Based

Define endpoints using decorators:

```python
@api_endpoint("/users/{id}", method="GET")
def get_user(id: int) -> User:
    pass
```

**Pros:**
- Pythonic syntax
- Good IDE support

**Cons:**
- Requires Python code for each endpoint
- Harder to share configurations
- Less flexible for dynamic APIs

### Option 3: Class-Based

Define endpoints as class methods:

```python
class MyAPI(APIClient):
    @get("/users/{id}")
    def get_user(self, id: int) -> User:
        pass
```

**Pros:**
- Good organization
- Type hints

**Cons:**
- Requires subclassing
- More boilerplate
- Less flexible

## Consequences

### Positive

1. **Simplicity**: Users only need to create a JSON file
2. **Flexibility**: Can support any REST API without code changes
3. **Shareability**: Configurations can be shared between projects
4. **Testability**: Easy to mock and test
5. **Maintainability**: Single codebase supports all APIs

### Negative

1. **Less IDE support**: No autocomplete for endpoint names
2. **Runtime validation**: Errors caught at runtime, not compile time
3. **Documentation**: Must generate docs from configs

### Mitigations

1. **CLI tools**: `apiforge doctor` validates configs
2. **Schema validation**: JSON Schema validates structure
3. **Detailed errors**: Clear error messages with suggestions

## References

- JSON Schema: https://json-schema.org/
- OpenAPI Specification: https://spec.openapis.org/
