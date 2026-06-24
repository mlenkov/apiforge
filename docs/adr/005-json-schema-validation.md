# ADR-005: JSON Schema Validation

## Status

Accepted

## Context

API configurations must follow a specific structure:

1. Required fields: `base_url`, `resources`
2. Resource structure: `path`, `method`, `parameters`
3. Parameter structure: `type`, `required`, `description`

Invalid configurations should fail fast with clear error messages.

## Decision

We will use **JSON Schema** for configuration validation:

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["base_url", "resources"],
  "properties": {
    "base_url": {
      "type": "string",
      "format": "uri"
    },
    "auth": {
      "type": "object",
      "properties": {
        "token": {"type": "string"},
        "api_key": {"type": "string"}
      }
    },
    "resources": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["path"],
        "properties": {
          "path": {"type": "string"},
          "method": {
            "type": "string",
            "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]
          }
        }
      }
    }
  }
}
```

### Implementation

```python
import jsonschema

def validate_config(config, schema):
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(config))
    
    if errors:
        # Format detailed error messages
        raise ApiForgeConfigError(format_errors(errors))
```

## Alternatives Considered

### Option 1: Manual Validation

Validate configuration manually:

```python
def validate_config(config):
    if "base_url" not in config:
        raise ApiForgeConfigError("Missing base_url")
    if "resources" not in config:
        raise ApiForgeConfigError("Missing resources")
    # ... more checks
```

**Pros:**
- No external dependency
- Full control over validation

**Cons:**
- Verbose code
- Hard to maintain
- Inconsistent error messages

### Option 2: Pydantic Models

Use Pydantic for validation:

```python
from pydantic import BaseModel

class Config(BaseModel):
    base_url: str
    resources: dict
```

**Pros:**
- Type safety
- Automatic serialization
- Good error messages

**Cons:**
- Heavy dependency
- Less flexible for dynamic structures
- Overkill for JSON configs

### Option 3: Dataclasses with Validation

Use dataclasses with custom validation:

```python
@dataclass
class Config:
    base_url: str
    resources: dict
    
    def __post_init__(self):
        if not self.base_url:
            raise ValueError("base_url required")
```

**Pros:**
- Pythonic
- Type hints
- No external dependency

**Cons:**
- Manual validation logic
- Less expressive than JSON Schema

## Consequences

### Positive

1. **Declarative**: Schema describes structure clearly
2. **Standard**: Uses widely-adopted JSON Schema standard
3. **Detailed Errors**: Provides path-specific error messages
4. **Extensible**: Easy to add new validation rules
5. **Tooling**: JSON Schema has many tools and validators

### Negative

1. **Dependency**: Adds `jsonschema` dependency
2. **Complexity**: JSON Schema can be complex
3. **Performance**: Schema validation has overhead

### Mitigations

1. **Optional**: Can fallback to manual validation if needed
2. **Cached**: Schema loaded once at startup
3. **Clear Errors**: Detailed error messages help debugging

## Implementation Details

### Error Formatting

```python
def format_errors(errors):
    messages = []
    for error in errors:
        path = ".".join(str(p) for p in error.absolute_path)
        messages.append(f"{path}: {error.message}")
    return "\n".join(messages)
```

Example output:
```
base_url: 'not-a-url' is not a valid URI
resources.users.method: 'INVALID' is not one of ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
```

### Schema Location

Schema stored at: `apiforge-configs/_template/api_template.json`

Loaded during config validation:
```python
def load_config(path):
    config = json.load(open(path))
    schema = json.load(open("apiforge-configs/_template/api_template.json"))
    validate_config(config, schema)
    return config
```

### Fallback Validation

If JSON Schema unavailable, fallback to manual validation:

```python
def validate_config(config):
    try:
        import jsonschema
        jsonschema.validate(config, schema)
    except ImportError:
        # Manual validation
        if "base_url" not in config:
            raise ApiForgeConfigError("Missing base_url")
```

## References

- JSON Schema: https://json-schema.org/
- jsonschema Library: https://python-jsonschema.readthedocs.io/
- Draft-07: https://json-schema.org/draft-07/json-schema-release-notes
