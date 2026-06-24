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
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
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
- pip or poetry

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

Use clear, descriptive commit messages:

```
Add pagination support for list endpoints

- Implement PaginationHelper class
- Add cursor-based pagination
- Update documentation

Closes #123
```

### Code Organization

```
apiforge/
├── __init__.py           # Public API
├── core/                 # Core functionality
│   ├── client.py         # Main client
│   ├── executor.py       # Request execution
│   ├── resource.py       # Resource handling
│   └── response.py       # Response wrapper
├── adapters/             # HTTP adapters
│   ├── base.py           # Abstract adapter
│   └── http.py           # HTTP implementation
├── serializers/          # Data serializers
│   ├── base.py           # Abstract serializer
│   └── json.py           # JSON implementation
├── config.py             # Configuration handling
├── cli.py                # CLI tools
└── exceptions.py         # Exception hierarchy
```

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

from apiforge import ApiForgeClient
from apiforge.exceptions import ApiForgeConfigError


@pytest.fixture
def sample_config():
    return {
        "base_url": "https://api.example.com",
        "resources": {
            "users": {"path": "/users", "method": "GET"}
        }
    }


class TestApiForgeClient:
    def test_client_creation(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        assert client is not None
    
    def test_client_no_config(self):
        with pytest.raises(ApiForgeConfigError):
            ApiForgeClient()
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Test both success and failure paths

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
- Use docstrings for all public classes and functions

Example:

```python
def get_resource(self, name: str) -> Resource:
    """Get a resource by name.

    Args:
        name: Name of the resource

    Returns:
        Resource object

    Raises:
        ApiForgeConfigError: If resource not found
    """
    if name not in self._resources:
        raise ApiForgeConfigError(f"Resource '{name}' not found")
    return self._resources[name]
```

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
- Updated `ApiForgeClient` to support pagination parameters
- Added documentation in `docs/pagination.md`

## Testing

- Added unit tests in `tests/test_pagination.py`
- Added integration tests in `tests/test_integration.py`
- Manual testing with Yandex Metrika API

## Breaking Changes

None. This is a backward-compatible addition.
```

### Review Process

1. PR will be reviewed by maintainers
2. Address any feedback
3. Once approved, PR will be merged

## Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create config with '...'
2. Run code '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., macOS, Windows]
- Python version: [e.g., 3.10]
- ApiForge version: [e.g., 0.1.0]

**Additional context**
Any other context about the problem.
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. "I'm always frustrated when..."

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions, feel free to:

1. Open an issue
2. Start a discussion
3. Reach out to maintainers

Thank you for contributing!
