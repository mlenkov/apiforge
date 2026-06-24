# ApiForge

[![CI](https://github.com/apiforge/apiforge/actions/workflows/ci.yml/badge.svg)](https://github.com/apiforge/apiforge/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/apiforge.svg)](https://pypi.org/project/apiforge/)
[![Python versions](https://img.shields.io/pypi/pyversions/apiforge.svg)](https://pypi.org/project/apiforge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Modern Python API Client Generator from JSON Configs.

## Features

- **JSON-based configuration** — Define API endpoints declaratively
- **Automatic parameter validation** — Required parameters enforced at runtime
- **Built-in retry logic** — Automatic retries with exponential backoff
- **Type-safe responses** — Structured response objects with lazy parsing
- **Extensible architecture** — Custom adapters and serializers
- **CLI tools** — Validate and manage configurations

## Installation

```bash
pip install apiforge
```

For async support:

```bash
pip install apiforge[async]
```

For development:

```bash
pip install apiforge[dev]
```

## Quick Start

### 1. Create a Configuration

Create a JSON config file for your API:

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "YOUR_API_TOKEN"
  },
  "resources": {
    "users": {
      "path": "/users",
      "method": "GET",
      "description": "List all users",
      "parameters": {
        "limit": {
          "type": "integer",
          "required": false,
          "description": "Max items to return"
        }
      }
    },
    "user": {
      "path": "/users/{user_id}",
      "method": "GET",
      "description": "Get user by ID",
      "parameters": {
        "user_id": {
          "type": "integer",
          "required": true,
          "description": "User ID"
        }
      }
    }
  }
}
```

### 2. Use the Client

```python
from apiforge import ApiForgeClient

# Create client from config file
client = ApiForgeClient(config_path="path/to/config.json")

# List available resources
print(client.list_resources())  # ['users', 'user']

# Make a request
response = client.request("users", params={"limit": 10})
print(response.json())

# Get a specific user
response = client.request("user", params={"user_id": 123})
print(response.json())

# Use convenience methods
response = client.get("users", params={"limit": 5})
```

### 3. Context Manager

```python
with ApiForgeClient(config_path="config.json") as client:
    response = client.request("users")
    print(response.json())
# Session automatically closed
```

## Configuration Reference

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base_url` | string | Yes | Base URL for all requests |
| `auth` | object | No | Authentication credentials |
| `default_headers` | object | No | Headers added to all requests |
| `resources` | object | Yes | API endpoint definitions |

### Authentication

```json
{
  "auth": {
    "token": "OAuth token",
    "api_key": "API key",
    "username": "Basic auth username",
    "password": "Basic auth password"
  }
}
```

### Resource Definition

```json
{
  "resources": {
    "resource_name": {
      "path": "/endpoint/{param}",
      "method": "GET",
      "description": "Human-readable description",
      "parameters": {
        "param": {
          "type": "string",
          "required": true,
          "description": "Parameter description",
          "default": "default_value"
        }
      },
      "headers": {
        "X-Custom-Header": "value"
      }
    }
  }
}
```

### Supported HTTP Methods

- `GET` (default)
- `POST`
- `PUT`
- `DELETE`
- `PATCH`

### Parameter Types

- `string`
- `integer`
- `number`
- `boolean`

## CLI Usage

### Validate Configurations

```bash
# Check all installed configs
apiforge doctor

# Check specific provider
apiforge doctor --provider yandex

# Check specific API
apiforge doctor --provider yandex --api metrika
```

### Install Default Configurations

```bash
apiforge install
```

This creates the directory structure at `~/.apiforge/configs/`.

## Advanced Usage

### Custom Adapter

```python
from apiforge.adapters.base import BaseAdapter
from apiforge.core.response import ApiForgeResponse

class CustomAdapter(BaseAdapter):
    def request(self, method, url, params=None, data=None, headers=None, **kwargs):
        # Your custom implementation
        response = your_http_library.request(method, url, ...)
        return ApiForgeResponse(
            status_code=response.status_code,
            content=response.content,
            headers=dict(response.headers)
        )

# Use custom adapter
from apiforge import ApiForgeClient
client = ApiForgeClient(config_path="config.json")
client._adapter = CustomAdapter()
```

### Custom Serializer

```python
from apiforge.serializers.base import BaseSerializer

class MsgPackSerializer(BaseSerializer):
    def dumps(self, obj):
        import msgpack
        return msgpack.packb(obj)
    
    def loads(self, data):
        import msgpack
        return msgpack.unpackb(data)
```

### Error Handling

```python
from apiforge import ApiForgeClient
from apiforge.exceptions import (
    ApiForgeError,
    ApiForgeRequestError,
    ApiForgeAuthenticationError,
    ApiForgeRateLimitError,
    ApiForgeResourceNotFoundError,
    ApiForgeConfigError,
)

try:
    client = ApiForgeClient(config_path="config.json")
    response = client.request("users")
except ApiForgeAuthenticationError:
    print("Authentication failed")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ApiForgeResourceNotFoundError:
    print("Resource not found")
except ApiForgeConfigError as e:
    print(f"Configuration error: {e}")
except ApiForgeRequestError as e:
    print(f"Request failed: {e.status_code}")
except ApiForgeError as e:
    print(f"ApiForge error: {e}")
```

## Examples

See the [examples](examples/) directory for complete usage examples:

- [Yandex Metrika](examples/yandex_metrika.py) — Working with Yandex Metrika API

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/apiforge/apiforge.git
cd apiforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
black .

# Type checking
mypy .
```

## Architecture

ApiForge follows a layered architecture:

```
┌─────────────────────────────────────┐
│           ApiForgeClient            │  ← User-facing API
├─────────────────────────────────────┤
│         ApiForgeExecutor            │  ← Coordinates requests
├─────────────────────────────────────┤
│           HTTPAdapter               │  ← Transport layer
├─────────────────────────────────────┤
│          requests library           │  ← HTTP implementation
└─────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Roadmap

- [x] Core client implementation
- [x] JSON configuration support
- [x] Retry logic with backoff
- [x] CLI tools
- [x] CI/CD pipeline
- [ ] Async support (httpx)
- [ ] Pagination helpers
- [ ] Rate limiting
- [ ] Caching
- [ ] Logging

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Support

- [GitHub Issues](https://github.com/apiforge/apiforge/issues)
- [Documentation](https://github.com/apiforge/apiforge#readme)
