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
- **Extensible architecture** — Custom adapters for any HTTP library
- **MCP-ready** — `on_before_request` hook for access control and token management
- **CLI tools** — Validate and manage configurations

## Installation

```bash
pip install apiforge
```

For development:

```bash
pip install apiforge[dev]
```

## Quick Start

### 1. Create a Configuration

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
from apiforge import Client

# Create client from config file
client = Client(config_path="path/to/config.json")

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
with Client(config_path="config.json") as client:
    response = client.request("users")
    print(response.json())
# Session automatically closed
```

## MCP Integration

ApiForge is designed as a transport core for MCP servers. Use the `on_before_request` hook for access control, token management, and audit logging:

```python
from apiforge import Client

def enforce_policy(method: str, url: str):
    """MCP policy: only allow GET requests."""
    if method != "GET":
        raise PermissionError("Read-only mode")

client = Client(
    config_path="config.json",
    on_before_request=enforce_policy
)
```

See [docs/adr/007-mcp-integration.md](docs/adr/007-mcp-integration.md) for architecture details.

## Configuration Reference

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base_url` | string | Yes | Base URL for all requests |
| `auth` | object | No | Authentication credentials |
| `default_headers` | object | No | Headers added to all requests |
| `resources` | object | Yes | API endpoint definitions |

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
          "description": "Parameter description"
        }
      }
    }
  }
}
```

### Supported HTTP Methods

`GET`, `POST`, `PUT`, `DELETE`, `PATCH`

## CLI Usage

```bash
# Validate all installed configs
apiforge doctor

# Check specific provider
apiforge doctor --provider yandex

# Install default configs
apiforge install
```

## Error Handling

```python
from apiforge import Client
from apiforge.exceptions import (
    ApiForgeError,
    ApiForgeRequestError,
    ApiForgeAuthenticationError,
    ApiForgeRateLimitError,
    ApiForgeResourceNotFoundError,
    ApiForgeConfigError,
)

try:
    client = Client(config_path="config.json")
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

## Backward Compatibility

Old import paths still work:

```python
# These all work (old style)
from apiforge import ApiForgeClient
from apiforge.core.client import ApiForgeClient
from apiforge.adapters.http import HTTPAdapter

# Recommended (new style)
from apiforge import Client
from apiforge.adapters import RequestsAdapter
```

## Project Structure

```
apiforge/
├── __init__.py              # Public API
├── client.py                # Client (main entry point)
├── executor.py              # Executor (coordinates adapter calls)
├── resource.py              # Resource (endpoint definition)
├── response.py              # Response (HTTP response wrapper)
├── exceptions.py            # Exception hierarchy
├── cli.py                   # CLI tools
├── config/                  # Configuration package
│   ├── loader.py            # load_config()
│   ├── validator.py         # JSON Schema validation
│   └── discovery.py         # get_config_path(), list_configs()
├── adapters/                # Transport layer
│   ├── base.py              # BaseAdapter (ABC)
│   └── requests_adapter.py  # RequestsAdapter (requests library)
└── core/                    # Backward-compat shims
```

## Examples

See the [examples](examples/) directory:
- [Yandex Metrika](examples/yandex_metrika.py) — Working with Yandex Metrika API
- [Bundled configs](configs/) — Pre-built configs for Yandex APIs

## Development

```bash
# Clone the repository
git clone https://github.com/apiforge/apiforge.git
cd apiforge

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Code quality
ruff check .
black --check .
mypy .
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Config    │  │  Resources  │  │      Executor       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Adapter Layer                            │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ BaseAdapter │  │ RequestsAdapter │  │  on_before_     │ │
│  │   (ABC)     │  │   (requests)    │  │  request hook   │ │
│  └─────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Documentation

- [Architecture](docs/architecture.md) — System design and patterns
- [Config Creation](docs/config-creation.md) — How to create configs (human guide)
- [Config Generation](docs/config-generation.md) — How to generate configs (AI guide)
- [ADR-001](docs/adr/001-config-driven-architecture.md) — Config-driven design
- [ADR-007](docs/adr/007-mcp-integration.md) — MCP server integration
- [ADR-008](docs/adr/008-access-control.md) — Access control architecture
- [Runbook](docs/runbook.md) — Operations and troubleshooting
- [Configuration](docs/configuration.md) — Config reference
- [FAQ](docs/faq.md) — Common questions

## Bundled Configs

Pre-built configs for Yandex APIs are in [`configs/`](configs/):

| API | Config | Resources |
|-----|--------|-----------|
| Metrika | `configs/yandex/metrika.json` | 52 |
| Direct | `configs/yandex/direct.json` | 30 |
| Audience | `configs/yandex/audience.json` | 54 |
| AdMetrica | `configs/yandex/admetrica.json` | 29 |
| Webmaster | `configs/yandex/webmaster.json` | 42 |

## Roadmap

- [x] Core client implementation
- [x] JSON configuration support
- [x] Retry logic with backoff
- [x] CLI tools
- [x] CI/CD pipeline
- [x] MCP integration hook
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
- [Security Policy](SECURITY.md)
