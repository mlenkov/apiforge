# Changelog

All notable changes to ApiForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Architecture documentation (`docs/architecture.md`)
- Architecture Decision Records (`docs/adr/`)
- Contributing guidelines (`CONTRIBUTING.md`)
- This changelog

### Changed

- Enhanced README with comprehensive documentation
- Improved error messages with suggestions

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
