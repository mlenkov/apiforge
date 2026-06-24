# Examples

This document provides comprehensive examples of using ApiForge.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Configuration Examples](#configuration-examples)
- [Error Handling](#error-handling)
- [Advanced Usage](#advanced-usage)
- [Integration Examples](#integration-examples)

## Basic Usage

### Simple Client

```python
from apiforge import ApiForgeClient

# Create client from config file
client = ApiForgeClient(config_path="config.json")

# Make a request
response = client.request("users")
print(response.json())
```

### Context Manager

```python
from apiforge import ApiForgeClient

with ApiForgeClient(config_path="config.json") as client:
    response = client.request("users")
    print(response.json())
# Session automatically closed
```

### Using Convenience Methods

```python
from apiforge import ApiForgeClient

client = ApiForgeClient(config_path="config.json")

# GET request
response = client.get("users", params={"limit": 10})

# POST request
response = client.post("users", data={"name": "John"})

# PUT request
response = client.put("users", data={"id": 1, "name": "John"})

# DELETE request
response = client.delete("users", params={"id": 1})

# PATCH request
response = client.patch("users", data={"name": "Jane"})
```

## Configuration Examples

### Basic Configuration

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "your-api-token"
  },
  "resources": {
    "users": {
      "path": "/users",
      "method": "GET",
      "description": "List all users"
    }
  }
}
```

### Configuration with Parameters

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "your-api-token"
  },
  "resources": {
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
    },
    "create_user": {
      "path": "/users",
      "method": "POST",
      "description": "Create a new user",
      "parameters": {
        "name": {
          "type": "string",
          "required": true,
          "description": "User name"
        },
        "email": {
          "type": "string",
          "required": true,
          "description": "User email"
        }
      }
    }
  }
}
```

### Configuration with Headers

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "your-api-token"
  },
  "default_headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "resources": {
    "users": {
      "path": "/users",
      "method": "GET",
      "headers": {
        "X-Custom-Header": "value"
      }
    }
  }
}
```

### Yandex Metrika Configuration

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
      "description": "Get statistics",
      "parameters": {
        "ids": {
          "type": "integer",
          "required": true,
          "description": "Counter ID"
        },
        "metrics": {
          "type": "string",
          "required": true,
          "description": "Metrics to retrieve"
        },
        "dimensions": {
          "type": "string",
          "required": false,
          "description": "Dimensions to group by"
        },
        "date1": {
          "type": "string",
          "required": false,
          "description": "Start date"
        },
        "date2": {
          "type": "string",
          "required": false,
          "description": "End date"
        }
      }
    },
    "counters": {
      "path": "/management/v1/counters",
      "method": "GET",
      "description": "List counters"
    }
  }
}
```

## Error Handling

### Basic Error Handling

```python
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeError

try:
    client = ApiForgeClient(config_path="config.json")
    response = client.request("users")
    print(response.json())
except ApiForgeError as e:
    print(f"ApiForge error: {e}")
```

### Specific Error Handling

```python
from apiforge import ApiForgeClient
from apiforge.exceptions import (
    ApiForgeAuthenticationError,
    ApiForgeRateLimitError,
    ApiForgeResourceNotFoundError,
    ApiForgeConfigError,
)

try:
    client = ApiForgeClient(config_path="config.json")
    response = client.request("users")
except ApiForgeAuthenticationError:
    print("Authentication failed. Check your API credentials.")
except ApiForgeRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds.")
except ApiForgeResourceNotFoundError:
    print("Resource not found.")
except ApiForgeConfigError as e:
    print(f"Configuration error: {e}")
```

### Retry Handling

```python
import time
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeRateLimitError

client = ApiForgeClient(
    config_path="config.json",
    max_retries=5,
    retry_delay=2.0
)

try:
    response = client.request("users")
except ApiForgeRateLimitError as e:
    print(f"Rate limited after {client._adapter.max_retries} retries")
    print(f"Retry-After header: {e.retry_after}")
```

## Advanced Usage

### Custom Adapter

```python
from apiforge.adapters.base import BaseAdapter
from apiforge.core.response import ApiForgeResponse

class CustomHTTPAdapter(BaseAdapter):
    def __init__(self, base_url="", auth=None, timeout=30.0):
        self.base_url = base_url
        self.auth = auth
        self.timeout = timeout
        # Initialize your HTTP client here
    
    def request(self, method, url, params=None, data=None, headers=None, **kwargs):
        # Build full URL
        full_url = f"{self.base_url}/{url.lstrip('/')}"
        
        # Make request with your HTTP client
        response = your_http_client.request(
            method=method,
            url=full_url,
            params=params,
            json=data,
            headers=headers,
            timeout=self.timeout
        )
        
        # Return ApiForgeResponse
        return ApiForgeResponse(
            status_code=response.status_code,
            content=response.content,
            headers=dict(response.headers)
        )

# Use custom adapter
from apiforge import ApiForgeClient

client = ApiForgeClient(config_path="config.json")
client._adapter = CustomHTTPAdapter(
    base_url="https://api.example.com",
    auth={"token": "your-token"}
)
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

# Use custom serializer
from apiforge.adapters.http import HTTPAdapter

adapter = HTTPAdapter(
    base_url="https://api.example.com",
    serializer=MsgPackSerializer()
)
```

### Dynamic Configuration

```python
import os
from apiforge import ApiForgeClient

# Build config dynamically
config = {
    "base_url": os.environ.get("API_BASE_URL", "https://api.example.com"),
    "auth": {
        "token": os.environ.get("API_TOKEN")
    },
    "resources": {
        "users": {
            "path": "/users",
            "method": "GET"
        }
    }
}

client = ApiForgeClient(config=config)
response = client.request("users")
```

### Pagination

```python
from apiforge import ApiForgeClient

client = ApiForgeClient(config_path="config.json")

# Simple pagination
page = 1
while True:
    response = client.request(
        "users",
        params={"page": page, "per_page": 100}
    )
    data = response.json()
    
    if not data:
        break
    
    for user in data:
        print(user["name"])
    
    page += 1
```

### Concurrent Requests

```python
import asyncio
from apiforge import ApiForgeClient

async def fetch_user(client, user_id):
    return client.request("user", params={"user_id": user_id})

async def main():
    client = ApiForgeClient(config_path="config.json")
    
    # Fetch multiple users concurrently
    tasks = [fetch_user(client, i) for i in range(1, 11)]
    responses = await asyncio.gather(*tasks)
    
    for response in responses:
        print(response.json())

asyncio.run(main())
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeError

app = FastAPI()

# Initialize client
client = ApiForgeClient(config_path="config.json")

@app.get("/users")
async def get_users():
    try:
        response = client.request("users")
        return response.json()
    except ApiForgeError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Django Integration

```python
from django.http import JsonResponse
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeError

# Initialize client
client = ApiForgeClient(config_path="config.json")

def get_users(request):
    try:
        response = client.request("users")
        return JsonResponse(response.json(), safe=False)
    except ApiForgeError as e:
        return JsonResponse({"error": str(e)}, status_code=500)
```

### CLI Tool

```python
import argparse
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeError

def main():
    parser = argparse.ArgumentParser(description="API Client")
    parser.add_argument("--config", required=True, help="Config file path")
    parser.add_argument("--resource", required=True, help="Resource name")
    parser.add_argument("--params", help="JSON params")
    
    args = parser.parse_args()
    
    try:
        client = ApiForgeClient(config_path=args.config)
        
        params = {}
        if args.params:
            import json
            params = json.loads(args.params)
        
        response = client.request(args.resource, params=params)
        print(response.json())
    except ApiForgeError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
```

### Testing

```python
import pytest
from unittest.mock import MagicMock, patch
from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeRequestError


@pytest.fixture
def mock_client():
    with patch("apiforge.adapters.http.HTTPAdapter.request") as mock_request:
        mock_request.return_value = MagicMock(
            status_code=200,
            content=b'{"users": []}',
            headers={"content-type": "application/json"}
        )
        
        client = ApiForgeClient(config={
            "base_url": "https://api.example.com",
            "resources": {
                "users": {"path": "/users", "method": "GET"}
            }
        })
        
        yield client, mock_request


def test_get_users(mock_client):
    client, mock_request = mock_client
    
    response = client.request("users")
    
    assert response.status_code == 200
    mock_request.assert_called_once()
```

## More Examples

See the [examples/](../examples/) directory for complete, runnable examples:

- [Yandex Metrika](../examples/yandex_metrika.py) - Working with Yandex Metrika API
