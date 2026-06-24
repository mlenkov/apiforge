# ADR-006: Serialization Layer Design

## Status

Accepted

## Context

APIs use different data formats:

1. JSON (most common)
2. MessagePack (binary, compact)
3. Protocol Buffers (binary, typed)
4. XML (legacy APIs)
5. YAML (configuration)

The library should support multiple serialization formats.

## Decision

We will implement a **Serialization Layer** with abstract base class:

```python
class BaseSerializer(ABC):
    @abstractmethod
    def dumps(self, obj) -> bytes:
        """Serialize object to bytes."""
        pass
    
    @abstractmethod
    def loads(self, data) -> Any:
        """Deserialize bytes to object."""
        pass

class JSONSerializer(BaseSerializer):
    def dumps(self, obj) -> bytes:
        return json.dumps(obj).encode("utf-8")
    
    def loads(self, data) -> Any:
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return json.loads(data)
```

## Alternatives Considered

### Option 1: Direct JSON Usage

Use `json` module directly:

```python
def request(self, ...):
    response = requests.request(...)
    return json.loads(response.content)
```

**Pros:**
- Simple implementation
- No abstraction overhead

**Cons:**
- Hard to swap formats
- No support for binary formats
- Tightly coupled to JSON

### Option 2: Content-Type Detection

Detect format from Content-Type header:

```python
def deserialize(self, content, content_type):
    if "json" in content_type:
        return json.loads(content)
    elif "msgpack" in content_type:
        return msgpack.unpackb(content)
```

**Pros:**
- Automatic format detection
- No configuration needed

**Cons:**
- Complex detection logic
- May fail on non-standard types
- Hard to customize

### Option 3: Plugin System

Use entry points for serializer plugins:

```python
# setup.py
entry_points={
    "apiforge.serializers": [
        "json = apiforge.serializers.json:JSONSerializer",
    ]
}
```

**Pros:**
- Extensible
- Third-party plugins possible

**Cons:**
- Complex implementation
- Harder to discover
- Overkill for most use cases

## Consequences

### Positive

1. **Flexibility**: Easy to add new formats
2. **Testability**: Can mock serializers
3. **Separation**: Serialization separate from transport
4. **Extensibility**: Users can add custom serializers

### Negative

1. **Abstraction**: Extra layer to understand
2. **Overhead**: Small performance cost
3. **Complexity**: More code to maintain

### Mitigations

1. **Default**: JSON works out of the box
2. **Simple Interface**: Only two methods to implement
3. **Documentation**: Clear examples for custom serializers

## Implementation Details

### JSONSerializer Features

- Handles strings, numbers, booleans, null
- Supports nested objects and arrays
- UTF-8 encoding by default
- Configurable options (indent, sort_keys)

### Usage in HTTPAdapter

```python
class HTTPAdapter(BaseAdapter):
    def __init__(self, serializer=None, ...):
        self.serializer = serializer or JSONSerializer()
    
    def request(self, method, url, data=None, ...):
        if data:
            data = self.serializer.dumps(data)
        
        response = self.session.request(...)
        
        return ApiForgeResponse(
            status_code=response.status_code,
            content=response.content,
            headers=dict(response.headers),
            serializer=self.serializer,
        )
```

### ApiForgeResponse Integration

```python
class ApiForgeResponse:
    def __init__(self, status_code, content, headers, serializer=None):
        self.serializer = serializer or JSONSerializer()
    
    def json(self):
        return self.serializer.loads(self.content)
    
    def text(self):
        return self.content.decode("utf-8")
```

## Custom Serializer Example

### MessagePack Serializer

```python
import msgpack

class MsgPackSerializer(BaseSerializer):
    def dumps(self, obj) -> bytes:
        return msgpack.packb(obj)
    
    def loads(self, data) -> Any:
        return msgpack.unpackb(data)

# Usage
adapter = HTTPAdapter(serializer=MsgPackSerializer())
```

### Protocol Buffers Serializer

```python
class ProtobufSerializer(BaseSerializer):
    def __init__(self, message_class):
        self.message_class = message_class
    
    def dumps(self, obj) -> bytes:
        message = self.message_class(**obj)
        return message.SerializeToString()
    
    def loads(self, data) -> Any:
        message = self.message_class()
        message.ParseFromString(data)
        return MessageToDict(message)
```

## References

- JSON: https://www.json.org/
- MessagePack: https://msgpack.org/
- Protocol Buffers: https://developers.google.com/protocol-buffers
