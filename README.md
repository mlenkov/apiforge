# ApiForge

Modern Python API Client Generator from JSON Configs.

## Installation

```bash
pip install apiforge
```

## Quick Start

```python
from apiforge import ApiForgeClient

# Create client from config file
client = ApiForgeClient(config_path="yandex/metrika.json")

# Make a request
response = client.request("stats", params={"ids": 123, "metrics": "ym:s:visits"})
print(response.json())
```

## Features

- JSON-based API configuration
- Automatic parameter validation
- Built-in retry logic
- Type-safe responses
- Easy to extend

## Configuration

Create a JSON config file:

```json
{
  "base_url": "https://api-metrika.yandex.net",
  "auth": {
    "token": "YOUR_OAUTH_TOKEN"
  },
  "resources": {
    "stats": {
      "path": "/stat/v1/data",
      "method": "GET",
      "parameters": {
        "ids": {"type": "integer", "required": true},
        "metrics": {"type": "string", "required": true}
      }
    }
  }
}
```

## CLI

```bash
# Check config integrity
apiforge doctor

# Check specific provider
apiforge doctor --provider yandex

# Install default configs
apiforge install
```

## License

MIT
