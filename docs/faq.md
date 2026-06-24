# Frequently Asked Questions

## Table of Contents

- [General](#general)
- [Configuration](#configuration)
- [Usage](#usage)
- [Errors](#errors)
- [Development](#development)

## General

### What is ApiForge?

ApiForge is a Python library for creating API clients from JSON configurations. Instead of writing code for each API endpoint, you define them in a JSON file, and ApiForge builds a typed client automatically.

### Why use ApiForge?

- **Simplicity**: Define APIs in JSON, no code required
- **Flexibility**: Works with any REST API
- **Maintainability**: Single codebase for all APIs
- **Reliability**: Built-in retry logic and error handling
- **Testability**: Easy to mock and test

### Is ApiForge production-ready?

ApiForge is in alpha (v0.1.0). It's stable enough for use but may have breaking changes in future versions.

### What Python versions are supported?

- Python 3.10
- Python 3.11
- Python 3.12

### What are the dependencies?

**Required:**
- `requests>=2.28.0`

**Optional:**
- `httpx>=0.24.0` (for async support)
- `jsonschema>=4.0.0` (for config validation)

## Configuration

### Where do I put my config file?

Anywhere you like! Common locations:

```
# Project directory
./configs/myapi.json

# Home directory
~/.apiforge/configs/myapi.json

# Any path
/path/to/config.json
```

### Can I use environment variables in config?

Yes! Use `${ENV_VAR}` syntax:

```json
{
  "auth": {
    "token": "${API_TOKEN}"
  }
}
```

Then resolve at runtime:

```python
import os
import json

def load_config(path):
    with open(path) as f:
        config = json.load(f)
    
    def resolve(obj):
        if isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            return os.environ.get(obj[2:-1], "")
        elif isinstance(obj, dict):
            return {k: resolve(v) for k, v in obj.items()}
        return obj
    
    return resolve(config)
```

### How do I validate my config?

Use the CLI:

```bash
apiforge doctor
```

Or programmatically:

```python
from apiforge.config import load_config

try:
    config = load_config("config.json")
except ApiForgeConfigError as e:
    print(f"Invalid config: {e}")
```

### Can I have multiple auth methods?

Yes, but only one will be used. The library uses the first available:

1. `token` (Bearer auth)
2. `api_key` (API key header)
3. `username`/`password` (Basic auth)

### What's the difference between `auth` and `default_headers`?

- `auth`: Authentication credentials (token, API key, basic auth)
- `default_headers`: Custom headers added to all requests

```json
{
  "auth": {
    "token": "your-token"
  },
  "default_headers": {
    "X-Custom-Header": "value"
  }
}
```

## Usage

### How do I make a request?

```python
from apiforge import ApiForgeClient

client = ApiForgeClient(config_path="config.json")
response = client.request("resource_name", params={...})
print(response.json())
```

### How do I pass path parameters?

Use `**kwargs` for path parameters:

```python
# Config: "path": "/users/{user_id}"
response = client.request("get_user", user_id=123)
```

### How do I pass query parameters?

Use `params` argument:

```python
response = client.request("list_users", params={"limit": 10, "offset": 0})
```

### How do I pass request body?

Use `data` argument:

```python
response = client.request("create_user", data={"name": "John", "email": "john@example.com"})
```

### How do I use convenience methods?

```python
# GET
response = client.get("users", params={"limit": 10})

# POST
response = client.post("users", data={"name": "John"})

# PUT
response = client.put("users", data={"id": 1, "name": "John"})

# DELETE
response = client.delete("users", params={"id": 1})

# PATCH
response = client.patch("users", data={"name": "Jane"})
```

### How do I access response data?

```python
response = client.request("users")

# JSON data
data = response.json()

# Text content
text = response.text()

# Status code
status = response.status_code

# Headers
headers = response.headers

# Check success
if response.ok:
    print("Success!")
```

### How do I use context managers?

```python
with ApiForgeClient(config_path="config.json") as client:
    response = client.request("users")
# Session automatically closed
```

### How do I list available resources?

```python
client = ApiForgeClient(config_path="config.json")
resources = client.list_resources()
print(resources)  # ['users', 'posts', 'comments']
```

## Errors

### How do I handle errors?

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
    print("Check your API credentials")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ApiForgeResourceNotFoundError:
    print("Resource not found")
except ApiForgeConfigError as e:
    print(f"Config error: {e}")
except ApiForgeRequestError as e:
    print(f"Request failed: {e.status_code}")
except ApiForgeError as e:
    print(f"Error: {e}")
```

### What does "Missing required parameters" mean?

You didn't provide a required parameter:

```python
# Wrong - missing user_id
response = client.request("get_user")

# Correct
response = client.request("get_user", params={"user_id": 123})
```

### What does "Resource not found" mean?

The resource name doesn't match your config:

```python
# Wrong - typo
response = client.request("user")  # Should be "get_user"

# Correct
response = client.request("get_user", params={"user_id": 123})
```

### What does "Rate limit exceeded" mean?

The API is rate limiting you. The library retries automatically, but you can handle it:

```python
from apiforge.exceptions import ApiForgeRateLimitError

try:
    response = client.request("users")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Wait {e.retry_after} seconds")
```

### What does "Authentication failed" mean?

Your credentials are invalid:

```python
# Check your config
{
  "auth": {
    "token": "your-valid-token"  # Make sure this is correct
  }
}
```

### What does "Connection error" mean?

Can't reach the API server:

1. Check your internet connection
2. Verify the `base_url` is correct
3. Check if the API is down

### What does "Request timeout" mean?

The request took too long:

```python
# Increase timeout
client = ApiForgeClient(
    config_path="config.json",
    timeout=60.0  # 60 seconds
)
```

## Development

### How do I set up development?

```bash
# Clone repo
git clone https://github.com/apiforge/apiforge.git
cd apiforge

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"
```

### How do I run tests?

```bash
pytest tests/ -v
```

### How do I run linting?

```bash
ruff check .
black --check .
mypy .
```

### How do I auto-fix linting issues?

```bash
ruff check --fix .
black .
```

### How do I add a new feature?

1. Create a branch: `git checkout -b feature/my-feature`
2. Make changes
3. Add tests
4. Run tests: `pytest tests/ -v`
5. Run linting: `ruff check . && black --check .`
6. Commit: `git commit -m "Add my feature"`
7. Push: `git push origin feature/my-feature`
8. Create PR

### How do I report a bug?

1. Check [GitHub Issues](https://github.com/apiforge/apiforge/issues)
2. If not found, create new issue
3. Include:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (OS, Python version, ApiForge version)

### How do I suggest a feature?

1. Check [GitHub Issues](https://github.com/apiforge/apiforge/issues)
2. If not found, create new issue with "feature request" label
3. Include:
   - Description of the feature
   - Use case
   - Proposed implementation (if any)

### Where can I get help?

- [Documentation](https://github.com/apiforge/apiforge#readme)
- [GitHub Issues](https://github.com/apiforge/apiforge/issues)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
