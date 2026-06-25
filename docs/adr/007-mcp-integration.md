# ADR-007: MCP Server Integration

## Status

Accepted

## Context

ApiForge will be used as the transport core for an MCP (Model Context Protocol) server. The MCP server exposes API tools to LLMs, which need to:
- Make HTTP requests to external APIs
- Handle authentication and token management
- Enforce access control (read-only vs read-write)
- Log all interactions for audit

## Decision

**Access control, token management, and role enforcement belong at the MCP layer, NOT in ApiForge core.**

ApiForge remains a policy-agnostic transport layer. The MCP server uses the `on_before_request` hook to enforce policies.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Tools     │  │   Policy    │  │   Token         │ │
│  │  (methods)  │  │  Engine     │  │   Manager       │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    ApiForge Core                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Client    │  │   Adapter   │  │   on_before_    │ │
│  │             │  │   (hook)    │  │   request       │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    External APIs                         │
└─────────────────────────────────────────────────────────┘
```

### Hook Usage

```python
from apiforge import Client

def enforce_policy(method: str, url: str):
    """MCP policy engine checks permissions."""
    if method != "GET" and not user_has_write_access():
        raise PermissionError("Read-only mode")
    
    if is_rate_limited(user_id):
        raise RateLimitError("Too many requests")

client = Client(
    config_path="config.json",
    on_before_request=enforce_policy
)
```

## Alternatives Considered

### Option 1: Policy in ApiForge Core

Add role-based access control directly in the adapter.

**Pros:**
- Single place for all logic

**Cons:**
- Violates separation of concerns
- ApiForge becomes opinionated
- Harder to test without API calls
- Doesn't work for non-MCP use cases

### Option 2: Middleware Pattern

Chain of responsibility pattern with policy middleware.

**Pros:**
- Flexible composition
- Reusable policies

**Cons:**
- Over-engineered for current needs
- Adds complexity without clear benefit

## Consequences

### Positive

1. **Separation of concerns**: ApiForge stays focused on transport
2. **Testability**: Policies can be tested independently
3. **Flexibility**: Different MCP servers can have different policies
4. **Simplicity**: No policy logic in the core library

### Negative

1. **No built-in access control**: Users must implement their own
2. **Hook coordination**: MCP must manage hook registration

### Mitigations

1. **Documentation**: Clear examples of policy implementation
2. **Type hints**: Hook signature is well-defined
3. **Error types**: Standard exceptions for policy violations

## References

- MCP Specification: https://spec.modelcontextprotocol.io/
- Hook pattern: https://en.wikipedia.org/wiki/Hook_(computer_programming)
