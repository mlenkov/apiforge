# ADR-008: Access Control Architecture

## Status

Accepted

## Context

When ApiForge is used as an MCP transport, different users/roles may have different permissions:
- **Read-only**: Can only make GET requests
- **Read-write**: Can make all requests
- **Admin**: Full access plus configuration changes

The access control must be enforced without modifying the core library.

## Decision

Access control is implemented via the `on_before_request` hook in the MCP layer.

### Permission Model

```python
from enum import Enum
from dataclasses import dataclass

class Permission(Enum):
    READ = "read"        # GET requests
    WRITE = "write"      # POST, PUT, DELETE, PATCH
    ADMIN = "admin"      # Configuration changes

@dataclass
class UserContext:
    user_id: str
    permissions: set[Permission]
    rate_limit: int  # requests per minute
```

### Policy Engine

```python
class PolicyEngine:
    def __init__(self, user_context: UserContext):
        self.context = user_context
    
    def check(self, method: str, url: str) -> bool:
        """Check if request is allowed."""
        if method == "GET":
            return Permission.READ in self.context.permissions
        else:
            return Permission.WRITE in self.context.permissions
```

### Integration

```python
from apiforge import Client

policy = PolicyEngine(user_context)

client = Client(
    config_path="config.json",
    on_before_request=policy.check
)
```

## Token Management

### Token Refresh

```python
class TokenManager:
    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._expires_at = 0
    
    def get_token(self) -> str:
        """Get valid token, refreshing if needed."""
        if time.time() > self._expires_at:
            self._refresh()
        return self._token
    
    def _refresh(self):
        """Refresh OAuth token."""
        response = requests.post(self.token_url, data={...})
        self._token = response.json()["access_token"]
        self._expires_at = time.time() + response.json()["expires_in"]

def ensure_valid_token(method: str, url: str):
    """Hook to ensure valid token before request."""
    token = token_manager.get_token()
    # Token is now valid, request will proceed
```

## Consequences

### Positive

1. **Flexibility**: Different policies for different users
2. **Separation**: Policy logic separate from transport
3. **Testability**: Policies can be unit tested
4. **Auditability**: All requests go through policy check

### Negative

1. **No built-in**: Must implement policy engine
2. **Performance**: Extra check per request (negligible)

## References

- RBAC: https://en.wikipedia.org/wiki/Role-based_access_control
- OAuth 2.0: https://oauth.net/2/
