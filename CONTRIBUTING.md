# Contributing to ApiForge

Thank you for your interest in contributing to ApiForge! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Architecture](#architecture)
- [License](#license)

## Code of Conduct

Please be respectful and inclusive in all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/apiforge.git
   cd apiforge
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Verify Setup

```bash
# Run tests
pytest tests/ -v

# Check code quality
ruff check .
black --check .
mypy .
```

## Making Changes

### Branch Naming

- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation changes
- `refactor/` — Code refactoring
- `test/` — Adding tests

### Commit Messages

Use clear, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add pagination support for list endpoints

- Implement PaginationHelper class
- Add cursor-based pagination
- Update documentation

Closes #123
```

Types:
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `style:` — Formatting (no code change)
- `refactor:` — Code restructuring
- `test:` — Adding tests
- `chore:` — Maintenance

### Code Organization

```
apiforge/
├── __init__.py              # Public API with backward-compat aliases
├── client.py                # Client (main entry point)
├── executor.py              # Executor (coordinates adapter calls)
├── resource.py              # Resource (endpoint definition)
├── response.py              # Response (HTTP response wrapper)
├── exceptions.py            # Exception hierarchy
├── cli.py                   # CLI tools
├── config/                  # Configuration package
│   ├── __init__.py          # Re-exports
│   ├── loader.py            # load_config()
│   ├── validator.py         # JSON Schema validation
│   └── discovery.py         # get_config_path(), list_configs()
├── adapters/                # Transport layer
│   ├── __init__.py
│   ├── base.py              # BaseAdapter (ABC) with on_before_request
│   └── requests_adapter.py  # RequestsAdapter (requests library)
├── core/                    # Backward-compat shims (do not modify)
└── serializers/             # Unused (dead code)
```

**Important**: The `core/` directory contains backward-compatibility shims. Do not add new code there — use the root-level modules instead.

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_client.py -v

# Run with coverage
pytest tests/ --cov=apiforge --cov-report=html
```

### Writing Tests

- Place tests in `tests/` directory
- Name files `test_*.py`
- Name functions `test_*`
- Use pytest fixtures for common setup
- Mock external dependencies

Example:

```python
import pytest
from unittest.mock import MagicMock, patch

from apiforge import Client
from apiforge.exceptions import ApiForgeConfigError


@pytest.fixture
def sample_config():
    return {
        "base_url": "https://api.example.com",
        "resources": {
            "users": {"path": "/users", "method": "GET"}
        }
    }


class TestClient:
    def test_client_creation(self, sample_config):
        client = Client(config=sample_config)
        assert client is not None
    
    def test_client_no_config(self):
        with pytest.raises(ApiForgeConfigError):
            Client()
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Test both success and failure paths
- Current: 250 tests passing

## Code Style

### Formatting

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Check formatting
black --check .

# Auto-format
black .
```

### Linting

We use [Ruff](https://github.com/astral-sh/ruff) for linting:

```bash
# Check linting
ruff check .

# Auto-fix
ruff check --fix .
```

### Type Checking

We use [mypy](https://mypy-lang.org/) for type checking:

```bash
mypy .
```

### Style Guidelines

- Line length: 88 characters (Black default)
- Use type hints for all public functions
- Follow PEP 8 for naming conventions
- No inline comments unless explaining "why" not "what"

## Pull Request Process

### Before Submitting

1. Ensure all tests pass:
   ```bash
   pytest tests/ -v
   ```

2. Ensure code quality checks pass:
   ```bash
   ruff check .
   black --check .
   mypy .
   ```

3. Update documentation if needed
4. Add tests for new functionality

### PR Description

Include:

1. **Summary**: Brief description of changes
2. **Motivation**: Why the change is needed
3. **Implementation**: How it was implemented
4. **Testing**: How it was tested
5. **Breaking Changes**: Any backward-incompatible changes

Example:

```markdown
## Summary

Add pagination support for list endpoints.

## Motivation

Currently, list endpoints return all results at once, which can be slow
for large datasets. This adds cursor-based pagination support.

## Implementation

- Added `PaginationHelper` class in `apiforge/helpers/pagination.py`
- Updated `Client` to support pagination parameters
- Added documentation in `docs/pagination.md`

## Testing

- Added unit tests in `tests/test_pagination.py`
- Added integration tests in `tests/test_integration.py`

## Breaking Changes

None. This is a backward-compatible addition.
```

### Review Process

1. PR will be reviewed by maintainers
2. Address any feedback
3. Once approved, PR will be merged

## Architecture

### Key Principles

1. **Separation of concerns**: Transport (ApiForge) separate from policy (MCP)
2. **Backward compatibility**: Old import paths must keep working
3. **Minimal surface area**: No unnecessary abstractions

### MCP Integration

When adding MCP-related features:
- Access control belongs in the MCP layer, not ApiForge core
- Use `on_before_request` hook for policy enforcement
- Keep the core library policy-agnostic

### Adding New Features

1. Check if feature belongs in core or MCP layer
2. If core: add to appropriate module
3. If MCP: implement in MCP server, use hooks
4. Add tests
5. Update documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions, feel free to:

1. Open an issue
2. Start a discussion
3. Reach out to maintainers

Thank you for contributing!
