# Configuration Guide

This guide explains how to configure ApiForge for your API.

## Table of Contents

- [Configuration File Format](#configuration-file-format)
- [Top-Level Fields](#top-level-fields)
- [Authentication](#authentication)
- [Resources](#resources)
- [Parameters](#parameters)
- [Validation](#validation)
- [Environment Variables](#environment-variables)
- [Multiple Configurations](#multiple-configurations)

## Configuration File Format

ApiForge uses JSON configuration files. Create a `.json` file with your API configuration:

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "your-api-token"
  },
  "resources": {
    "endpoint_name": {
      "path": "/endpoint",
      "method": "GET"
    }
  }
}
```

## Top-Level Fields

### base_url (Required)

The base URL for all API requests.

```json
{
  "base_url": "https://api.example.com"
}
```

**Requirements:**
- Must be a valid URI
- Should use HTTPS
- No trailing slash

### auth (Optional)

Authentication credentials. Supports multiple auth methods:

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

### default_headers (Optional)

Headers added to all requests:

```json
{
  "default_headers": {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Custom-Header": "value"
  }
}
```

### resources (Required)

API endpoint definitions. Each resource represents an API endpoint:

```json
{
  "resources": {
    "endpoint_name": {
      "path": "/endpoint",
      "method": "GET",
      "description": "Human-readable description",
      "parameters": {},
      "headers": {}
    }
  }
}
```

## Authentication

### OAuth Token

```json
{
  "auth": {
    "token": "your-oauth-token"
  }
}
```

Used with `Authorization: Bearer <token>` header.

### API Key

```json
{
  "auth": {
    "api_key": "your-api-key"
  }
}
```

Used with `X-API-Key: <key>` header.

### Basic Auth

```json
{
  "auth": {
    "username": "user",
    "password": "pass"
  }
}
```

Used with `Authorization: Basic <base64>` header.

### No Authentication

```json
{
  "auth": {}
}
```

Or omit the `auth` field entirely.

## Resources

### Resource Definition

```json
{
  "resources": {
    "resource_name": {
      "path": "/path/{param}",
      "method": "GET",
      "description": "Description of the endpoint",
      "parameters": {
        "param": {
          "type": "string",
          "required": true,
          "description": "Parameter description"
        }
      },
      "headers": {
        "X-Custom-Header": "value"
      }
    }
  }
}
```

### Resource Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | Endpoint path (supports `{param}` placeholders) |
| `method` | string | No | HTTP method (default: "GET") |
| `description` | string | No | Human-readable description |
| `parameters` | object | No | Parameter definitions |
| `headers` | object | No | Request-specific headers |

### Path Parameters

Use `{param_name}` placeholders in paths:

```json
{
  "resources": {
    "user": {
      "path": "/users/{user_id}",
      "method": "GET"
    },
    "user_posts": {
      "path": "/users/{user_id}/posts/{post_id}",
      "method": "GET"
    }
  }
}
```

### HTTP Methods

Supported methods:

- `GET` (default)
- `POST`
- `PUT`
- `DELETE`
- `PATCH`

```json
{
  "resources": {
    "list_users": {
      "path": "/users",
      "method": "GET"
    },
    "create_user": {
      "path": "/users",
      "method": "POST"
    },
    "update_user": {
      "path": "/users/{user_id}",
      "method": "PUT"
    },
    "delete_user": {
      "path": "/users/{user_id}",
      "method": "DELETE"
    },
    "patch_user": {
      "path": "/users/{user_id}",
      "method": "PATCH"
    }
  }
}
```

### Resource-Specific Headers

Add headers to specific resources:

```json
{
  "resources": {
    "admin_endpoint": {
      "path": "/admin/users",
      "method": "GET",
      "headers": {
        "X-Admin-Token": "admin-secret"
      }
    }
  }
}
```

## Parameters

### Parameter Definition

```json
{
  "parameters": {
    "param_name": {
      "type": "string",
      "required": true,
      "description": "Parameter description",
      "default": "default_value"
    }
  }
}
```

### Parameter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | No | Data type (string, integer, number, boolean) |
| `required` | boolean | No | Whether parameter is required (default: false) |
| `description` | string | No | Human-readable description |
| `default` | any | No | Default value |

### Parameter Types

#### String

```json
{
  "name": {
    "type": "string",
    "required": true,
    "description": "User name"
  }
}
```

#### Integer

```json
{
  "user_id": {
    "type": "integer",
    "required": true,
    "description": "User ID"
  }
}
```

#### Number

```json
{
  "price": {
    "type": "number",
    "required": true,
    "description": "Product price"
  }
}
```

#### Boolean

```json
{
  "active": {
    "type": "boolean",
    "required": false,
    "description": "Is user active",
    "default": true
  }
}
```

### Required vs Optional Parameters

```json
{
  "parameters": {
    "required_param": {
      "type": "string",
      "required": true
    },
    "optional_param": {
      "type": "string",
      "required": false
    }
  }
}
```

**Note:** Required parameters must be provided in requests or an error is raised.

### Default Values

```json
{
  "parameters": {
    "limit": {
      "type": "integer",
      "required": false,
      "default": 10
    }
  }
}
```

## Validation

### Automatic Validation

ApiForge validates configurations automatically:

```python
from apiforge import Client

try:
    client = Client(config_path="config.json")
except ApiForgeConfigError as e:
    print(f"Invalid configuration: {e}")
```

### Validation Rules

1. **base_url**: Must be present and valid URI
2. **resources**: Must be present and non-empty
3. **path**: Each resource must have a path
4. **method**: Must be one of GET, POST, PUT, DELETE, PATCH
5. **type**: Parameters must have valid types
6. **required**: Must be boolean if present

### Validation Errors

```json
{
  "error": "Configuration validation failed",
  "details": [
    {
      "path": "base_url",
      "message": "'not-a-url' is not a valid URI"
    },
    {
      "path": "resources.users.method",
      "message": "'INVALID' is not one of ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']"
    }
  ]
}
```

### Using CLI for Validation

```bash
# Validate all configs
apiforge doctor

# Validate specific provider
apiforge doctor --provider yandex

# Validate specific API
apiforge doctor --provider yandex --api metrika
```

## Environment Variables

### Using Environment Variables

Use `${ENV_VAR}` syntax for environment variables:

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  }
}
```

### Resolving Environment Variables

```python
import os
import json

def load_config_with_env(path):
    with open(path) as f:
        config = json.load(f)
    
    def resolve_env(obj):
        if isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            return os.environ.get(env_var, "")
        elif isinstance(obj, dict):
            return {k: resolve_env(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_env(item) for item in obj]
        return obj
    
    return resolve_env(config)

# Usage
config = load_config_with_env("config.json")
client = Client(config=config)
```

### Setting Environment Variables

```bash
# Linux/macOS
export API_TOKEN="your-token"

# Windows
set API_TOKEN=your-token

# PowerShell
$env:API_TOKEN="your-token"
```

## Multiple Configurations

### Separate Config Files

Create separate files for different environments:

```
configs/
├── development.json
├── staging.json
└── production.json
```

### Loading Different Configs

```python
import os
from apiforge import Client

env = os.environ.get("ENV", "development")
config_path = f"configs/{env}.json"

client = Client(config_path=config_path)
```

### Config Directory Structure

```
~/.apiforge/configs/
├── yandex/
│   ├── metrika.json
│   └── direct.json
├── google/
│   └── analytics.json
└── github/
    └── api.json
```

### Loading from Default Location

```python
from apiforge.config import get_config_path, load_config

# Get path for provider/api
path = get_config_path("yandex", "metrika")
# Returns: ~/.apiforge/configs/yandex/metrika.json

# Load config
config = load_config(path)
client = Client(config=config)
```

## Complete Example

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  },
  "default_headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
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
          "description": "Max items to return",
          "default": 10
        },
        "offset": {
          "type": "integer",
          "required": false,
          "description": "Number of items to skip",
          "default": 0
        }
      }
    },
    "get_user": {
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
    },
    "update_user": {
      "path": "/users/{user_id}",
      "method": "PUT",
      "description": "Update a user",
      "parameters": {
        "user_id": {
          "type": "integer",
          "required": true,
          "description": "User ID"
        },
        "name": {
          "type": "string",
          "required": false,
          "description": "User name"
        },
        "email": {
          "type": "string",
          "required": false,
          "description": "User email"
        }
      }
    },
    "delete_user": {
      "path": "/users/{user_id}",
      "method": "DELETE",
      "description": "Delete a user",
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

## Troubleshooting

### Common Issues

#### "Missing required parameters"

Ensure all required parameters are provided:

```python
# Wrong - missing required user_id
response = client.request("get_user")

# Correct
response = client.request("get_user", params={"user_id": 123})
```

#### "Resource not found"

Check resource name matches config:

```python
# Wrong - typo in resource name
response = client.request("user")  # Should be "get_user"

# Correct
response = client.request("get_user", params={"user_id": 123})
```

#### "Invalid configuration"

Validate your config:

```bash
apiforge doctor
```

### Getting Help

- Check the [FAQ](faq.md)
- Search [GitHub Issues](https://github.com/apiforge/apiforge/issues)
- Open a new issue
