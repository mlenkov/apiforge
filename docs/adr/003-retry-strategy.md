# ADR-003: Retry Strategy with Backoff

## Status

Accepted

## Context

REST APIs can fail temporarily due to:

1. Rate limiting (429 Too Many Requests)
2. Server errors (5xx)
3. Network issues (connection errors, timeouts)

The library should handle these gracefully without user intervention.

## Decision

We will implement **automatic retries with linear backoff**:

### Retry Rules

| Error Type | Behavior |
|------------|----------|
| 401 Unauthorized | Immediate failure |
| 404 Not Found | Immediate failure |
| 429 Rate Limited | Retry after `Retry-After` header or delay |
| 5xx Server Error | Retry with backoff |
| Connection Error | Retry with backoff |
| Timeout | Retry with backoff |

### Backoff Formula

```python
delay = retry_delay * (attempt + 1)
```

Example with `retry_delay=1.0`:
- Attempt 0: 1 second
- Attempt 1: 2 seconds
- Attempt 2: 3 seconds

### Configuration

```python
adapter = HTTPAdapter(
    max_retries=3,      # Maximum retry attempts
    retry_delay=1.0,    # Base delay in seconds
)
```

## Alternatives Considered

### Option 1: No Retries

Fail immediately on any error.

**Pros:**
- Simple implementation
- Fast failure

**Cons:**
- Users must handle retries manually
- Poor experience for transient errors

### Option 2: Exponential Backoff

```python
delay = retry_delay * (2 ** attempt)
```

**Pros:**
- More aggressive backoff
- Better for high traffic

**Cons:**
- Can lead to very long waits
- May be too aggressive for most APIs

### Option 3: Fixed Delay

```python
delay = retry_delay  # Always same delay
```

**Pros:**
- Predictable behavior
- Simple implementation

**Cons:**
- Can overwhelm servers
- Not respectful of rate limits

### Option 4: Configurable Strategy

Allow users to provide custom retry logic:

```python
def my_retry_strategy(attempt, error):
    return attempt * 2  # Custom delay

adapter = HTTPAdapter(retry_strategy=my_retry_strategy)
```

**Pros:**
- Maximum flexibility
- Users can implement any strategy

**Cons:**
- More complex API
- Harder to document
- Most users don't need this

## Consequences

### Positive

1. **Resilience**: Handles transient errors automatically
2. **User Experience**: Users don't need to implement retry logic
3. **Rate Limit Respect**: Honors `Retry-After` headers
4. **Configurable**: Users can adjust max retries and delay

### Negative

1. **Latency**: Retries add latency
2. **Resource Usage**: Retries consume resources
3. **Unpredictable**: Hard to predict exact timing

### Mitigations

1. **Default Limits**: Reasonable defaults (3 retries, 1s delay)
2. **Immediate Failures**: Don't retry client errors (4xx)
3. **Configurable**: Users can adjust or disable retries

## Implementation Details

### Error Handling Flow

```python
def request(self, method, url, ...):
    for attempt in range(max_retries + 1):
        try:
            response = self.session.request(method, url, ...)
            
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", retry_delay)
                if attempt < max_retries:
                    time.sleep(retry_after)
                    continue
                raise ApiForgeRateLimitError(...)
            
            if response.status_code >= 500 and attempt < max_retries:
                time.sleep(retry_delay * (attempt + 1))
                continue
            
            # Handle other status codes
            
        except ConnectionError as e:
            if attempt < max_retries:
                time.sleep(retry_delay * (attempt + 1))
                continue
            raise ApiForgeRequestError(...)
```

### Rate Limiting

For 429 responses:
1. Read `Retry-After` header (seconds)
2. Fall back to `retry_delay` if header missing
3. Sleep for specified duration
4. Retry request

## References

- HTTP 429: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
- Retry-After: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
- Exponential Backoff: https://en.wikipedia.org/wiki/Exponential_backoff
