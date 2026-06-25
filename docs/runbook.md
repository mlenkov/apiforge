# Runbook

Operational procedures for ApiForge.

## Table of Contents

- [Quick Start](#quick-start)
- [Configuration Management](#configuration-management)
- [CLI Commands](#cli-commands)
- [Troubleshooting](#troubleshooting)
- [MCP Integration](#mcp-integration)
- [Monitoring](#monitoring)

## Quick Start

### Installation

```bash
pip install apiforge

# With async support
pip install apiforge[async]

# For development
pip install apiforge[dev]
```

### Basic Usage

```python
from apiforge import Client

# From config file
client = Client(config_path="config.json")
response = client.request("users", params={"limit": 10})

# From dict
client = Client(config={
    "base_url": "https://api.example.com",
    "resources": {
        "users": {"path": "/users", "method": "GET"}
    }
})
response = client.request("users")
```

## Configuration Management

### Config File Locations

1. **Project-local**: `./config.json`
2. **User-level**: `~/.apiforge/configs/<provider>/<api>.json`

### Installing Default Configs

```bash
apiforge install
```

Creates directory structure at `~/.apiforge/configs/`.

### Validating Configs

```bash
# Check all installed configs
apiforge doctor

# Check specific provider
apiforge doctor --provider yandex

# Check specific API
apiforge doctor --provider yandex --api metrika
```

### Creating Custom Configs

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  },
  "default_headers": {
    "X-Custom": "value"
  },
  "resources": {
    "list_users": {
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
    "get_user": {
      "path": "/users/{user_id}",
      "method": "GET",
      "description": "Get user by ID",
      "parameters": {
        "user_id": {
          "type": "string",
          "required": true,
          "description": "User ID"
        }
      }
    }
  }
}
```

## CLI Commands

### doctor

Check integrity of installed configurations.

```bash
# Check all
apiforge doctor

# Check provider
apiforge doctor --provider yandex

# Check specific API
apiforge doctor --provider yandex --api metrika
```

Exit codes:
- `0`: All checks passed
- `1`: Errors found

### install

Install default configuration files.

```bash
apiforge install
```

Creates `~/.apiforge/configs/` directory structure.

## Troubleshooting

### Common Issues

#### "Config file not found"

```bash
apiforge doctor --provider yandex --api metrika
# Output: Config file not found: ~/.apiforge/configs/yandex/metrika.json
```

**Solution**: Run `apiforge install` or manually create the config file.

#### "Invalid JSON in config file"

```bash
apiforge doctor --provider yandex --api metrika
# Output: Invalid JSON in config file: ...
```

**Solution**: Validate JSON syntax. Use `python -m json.tool config.json`.

#### "Configuration validation failed"

```bash
apiforge doctor --provider yandex --api metrika
# Output: Configuration validation failed: [resources.users] 'path' is a required property
```

**Solution**: Check config structure against schema. See `examples/configs/_template/api_template.json`.

#### "Missing required parameters"

```python
client.request("get_user")  # Raises ApiForgeConfigError
```

**Solution**: Pass required parameters:

```python
client.request("get_user", params={"user_id": "123"})
```

#### "Resource not found"

```python
client.request("nonexistent")  # Raises ApiForgeConfigError
```

**Solution**: Check available resources:

```python
print(client.list_resources())
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

client = Client(config_path="config.json")
```

### Network Issues

#### Connection Errors

```python
from apiforge import Client
from apiforge.exceptions import ApiForgeRequestError

try:
    client = Client(config_path="config.json")
    response = client.request("users")
except ApiForgeRequestError as e:
    if "Connection error" in str(e):
        print("Check network connection")
    elif "timeout" in str(e):
        print("Request timed out")
```

#### Rate Limiting

```python
from apiforge.exceptions import ApiForgeRateLimitError

try:
    response = client.request("users")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
    time.sleep(e.retry_after)
    response = client.request("users")
```

## MCP Integration

### Setting Up Access Control

```python
from apiforge import Client

class PolicyEngine:
    def __init__(self, allowed_methods=None):
        self.allowed_methods = allowed_methods or {"GET"}
    
    def check(self, method: str, url: str):
        if method not in self.allowed_methods:
            raise PermissionError(f"Method {method} not allowed")

# Read-only mode
policy = PolicyEngine(allowed_methods={"GET"})
client = Client(
    config_path="config.json",
    on_before_request=policy.check
)
```

### Token Management

```python
import time
import requests
from apiforge import Client

class TokenManager:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._expires_at = 0
    
    def get_token(self):
        if time.time() > self._expires_at:
            self._refresh()
        return self._token
    
    def _refresh(self):
        response = requests.post(self.token_url, data={
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.time() + data["expires_in"]

token_manager = TokenManager(
    token_url="https://auth.example.com/token",
    client_id="my_client_id",
    client_secret="my_client_secret"
)

def refresh_before_request(method: str, url: str):
    token = token_manager.get_token()

client = Client(
    config_path="config.json",
    on_before_request=refresh_before_request
)
```

### Audit Logging

```python
import logging
from apiforge import Client

logger = logging.getLogger("mcp.audit")

def audit_log(method: str, url: str):
    logger.info(f"MCP request: {method} {url}")

client = Client(
    config_path="config.json",
    on_before_request=audit_log
)
```

## Monitoring

### Health Check

```python
from apiforge import Client

def health_check(config_path):
    try:
        client = Client(config_path=config_path)
        resources = client.list_resources()
        return {"status": "healthy", "resources": len(resources)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Metrics Collection

```python
import time
from apiforge import Client

metrics = {
    "requests_total": 0,
    "requests_success": 0,
    "requests_failed": 0,
    "request_duration_sum": 0,
}

def collect_metrics(method: str, url: str):
    metrics["requests_total"] += 1
    # Duration measured elsewhere

client = Client(
    config_path="config.json",
    on_before_request=collect_metrics
)
```

### Error Tracking

```python
from apiforge import Client
from apiforge.exceptions import ApiForgeError

def track_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiForgeError as e:
            # Send to error tracking service
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
```

## Reference

- [Architecture](architecture.md)
- [Configuration](configuration.md)
- [Examples](examples.md)
- [FAQ](faq.md)
