# Changelog

All notable changes to ApiForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- ADR-007: MCP Server Integration (`docs/adr/007-mcp-integration.md`)
- ADR-008: Access Control Architecture (`docs/adr/008-access-control.md`)
- `on_before_request` hook in BaseAdapter for MCP policy enforcement
- Resource method validation (must be GET/POST/PUT/DELETE/PATCH)
- Response encoding fallback (UTF-8 → latin-1)
- Retry-After header parsing with error handling
- Backward-compatibility shims for old import paths

### Changed

- **BREAKING**: Renamed `ApiForgeClient` → `Client` (old name still works as alias)
- **BREAKING**: Renamed `ApiForgeResponse` → `Response` (old name still works as alias)
- **BREAKING**: Renamed `ApiForgeExecutor` → `Executor` (old name still works as alias)
- **BREAKING**: Renamed `HTTPAdapter` → `RequestsAdapter` (old name still works as alias)
- Moved `core/` modules to package root (`apiforge/client.py`, etc.)
- Split `config.py` into `config/` package (loader, validator, discovery)
- Moved `apiforge-configs/` → `examples/configs/`
- Updated architecture documentation for MCP integration
- Updated CONTRIBUTING.md with new code structure
- Updated SECURITY.md with MCP security considerations

### Fixed

- Resource mutation in convenience methods (get/post/put/delete/patch)
- Dead `url` variable in `client.request()`
- Response decode fallback (was UnicodeDecodeError, now falls back to latin-1)
- Duplicate TestGetConfigPath/TestListConfigs classes in test_config.py
- Retry-After header parsing crash on non-numeric values

### Removed

- Unused executor parameters (base_url, auth, etc.) — executor uses adapter
- Duplicate except blocks in RequestsAdapter (was 4 redundant re-raises)

## [0.1.0] - 2024-01-01

### Added

#### Core Features

- **ApiForgeClient**: Main client class for API interactions
- **ApiForgeExecutor**: Request execution with retry logic
- **HTTPAdapter**: HTTP transport using requests library
- **Resource**: API endpoint definition and validation
- **ApiForgeResponse**: Response wrapper with lazy parsing

#### Configuration

- JSON-based configuration support
- JSON Schema validation for configurations
- Config discovery and management
- CLI tools for config validation

#### Error Handling

- Comprehensive exception hierarchy
- Detailed error messages with context
- Automatic retry with backoff for transient errors

#### CLI

- `apiforge doctor` - Validate configurations
- `apiforge install` - Install default configs

#### Testing

- Unit tests for all core components
- Integration tests for end-to-end flows
- 117 tests with full coverage

#### CI/CD

- GitHub Actions workflow for testing
- Automated PyPI publishing
- Code coverage reporting

### Fixed

- Architectural contradiction between executor and adapter
- Adapter now properly handles retries and error handling
- Executor delegates to adapter for all HTTP operations

### Changed

- HTTPAdapter is now the transport layer with retry logic
- ApiForgeExecutor is now a coordinator, not a direct HTTP client
- ApiForgeClient creates adapter by default

## [0.0.1] - 2023-12-01

### Added

- Initial project structure
- Basic client implementation
- Configuration loading
- Initial test suite

[Unreleased]: https://github.com/apiforge/apiforge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/apiforge/apiforge/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/apiforge/apiforge/releases/tag/v0.0.1
