# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within ApiForge, please send an email to the maintainers. All security vulnerabilities will be promptly addressed.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to include

When reporting a vulnerability, please include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix**: Depends on severity, typically within 2 weeks

## Security Best Practices

When using ApiForge:

1. **Never commit credentials** to version control
2. **Use environment variables** for API tokens
3. **Validate configurations** before use
4. **Keep dependencies updated**
5. **Use HTTPS** for all API endpoints

### Secure Configuration Example

```python
import os
from apiforge import ApiForgeClient

# Use environment variables for sensitive data
client = ApiForgeClient(
    config_path="config.json",
    auth={"token": os.environ.get("API_TOKEN")}
)
```

### Configuration File Best Practices

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  },
  "resources": { ... }
}
```

Use `${ENV_VAR}` syntax and resolve at runtime:

```python
import os
import json

def load_config_with_env(path):
    with open(path) as f:
        config = json.load(f)
    
    # Resolve environment variables
    if "auth" in config and "token" in config["auth"]:
        token = config["auth"]["token"]
        if token.startswith("${") and token.endswith("}"):
            env_var = token[2:-1]
            config["auth"]["token"] = os.environ.get(env_var, "")
    
    return config
```

## Dependency Security

### Checking Dependencies

```bash
# Check for known vulnerabilities
pip audit

# Or with safety
safety check
```

### Keeping Dependencies Updated

```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Or with pip-tools
pip-compile --upgrade requirements.in
```

## Logging Sensitive Data

**Never log sensitive data** such as:

- API tokens
- Passwords
- Personal information

### Safe Logging Example

```python
import logging

logger = logging.getLogger(__name__)

# Safe - logs only non-sensitive info
logger.info("Making request to %s", url)

# Unsafe - logs sensitive data
logger.debug("Request headers: %s", headers)  # May contain auth token
```

## Network Security

### HTTPS Only

Always use HTTPS endpoints:

```json
{
  "base_url": "https://api.example.com"
}
```

### Certificate Verification

The `requests` library verifies SSL certificates by default. Never disable verification:

```python
# Good - verification enabled (default)
response = requests.get(url)

# Bad - verification disabled
response = requests.get(url, verify=False)  # Don't do this!
```

## Reporting Security Issues

For security issues, please contact:

- Email: security@apiforge.dev (example)
- GitHub Security Advisories: https://github.com/apiforge/apiforge/security/advisories

Thank you for helping keep ApiForge secure!
