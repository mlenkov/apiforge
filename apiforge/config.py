"""Config module for ApiForge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, ValidationError

from .exceptions import ApiForgeConfigError


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load configuration from a JSON file.

    Args:
        config_path: Path to the JSON config file

    Returns:
        Configuration dictionary

    Raises:
        ApiForgeConfigError: If config file is invalid or not found
    """
    path = Path(config_path)

    if not path.exists():
        raise ApiForgeConfigError(f"Config file not found: {path}")

    if not path.suffix.lower() == ".json":
        raise ApiForgeConfigError(
            f"Unsupported config format: {path.suffix}. Only JSON is supported."
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ApiForgeConfigError(f"Invalid JSON in config file: {e}") from e
    except Exception as e:
        raise ApiForgeConfigError(f"Failed to read config file: {e}") from e

    _validate_config(config)
    return config


def _get_schema() -> dict[str, Any]:
    """Load JSON Schema from template."""
    schema_path = (
        Path.home() / ".apiforge" / "configs" / "_template" / "api_template.json"
    )
    if not schema_path.exists():
        schema_path = Path(__file__).parent.parent / "apiforge-configs" / "_template" / "api_template.json"
    if not schema_path.exists():
        raise ApiForgeConfigError("Cannot find schema template file")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _format_error_path(path: list[str]) -> str:
    """Format JSON Schema error path to human-readable string."""
    if not path:
        return "root"
    parts = []
    for part in path:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(part)
    return "".join(parts)


def _get_suggestion(error: ValidationError) -> str:
    """Generate suggestion based on validation error."""
    path = _format_error_path(list(error.absolute_path))
    validator = error.validator
    value = error.instance

    if validator == "required":
        missing = error.message.split("'")[1] if "'" in error.message else "field"
        return f"Add '{missing}' to the configuration"

    if validator == "type":
        expected = error.message.split("'")[1] if "'" in error.message else "value"
        return f"Change '{path}' to be of type '{expected}'"

    if validator == "enum":
        allowed = error.message.split("[")[1].split("]")[0] if "[" in error.message else "valid values"
        return f"Use one of: {allowed}"

    if validator == "format":
        expected = error.message.split("'")[1] if "'" in error.message else "valid format"
        return f"Ensure '{path}' is a valid {expected}"

    if validator == "additionalProperties":
        return f"Remove unexpected property '{path}'"

    return "Check the configuration documentation"


def _validate_uri_format(config: dict[str, Any]) -> list[str]:
    """Validate URI format for base_url field."""
    errors = []
    base_url = config.get("base_url")
    if base_url and not isinstance(base_url, str):
        return errors
    if base_url:
        from urllib.parse import urlparse
        try:
            result = urlparse(base_url)
            if not all([result.scheme, result.netloc]):
                errors.append(f"base_url must be a valid URI (e.g., https://api.example.com)")
        except Exception:
            errors.append(f"base_url must be a valid URI (e.g., https://api.example.com)")
    return errors


def _validate_config(config: dict[str, Any]) -> None:
    """Validate config using JSON Schema."""
    try:
        schema = _get_schema()
    except Exception:
        _validate_config_fallback(config)
        return

    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(config))

    uri_errors = _validate_uri_format(config)
    for uri_err in uri_errors:
        from jsonschema import ValidationError as VE
        errors.append(VE(uri_err, validator="format", instance=config.get("base_url"), schema_path=["properties", "base_url", "format"]))

    if not errors:
        return

    error_messages = []
    for error in errors[:5]:
        path = _format_error_path(list(error.absolute_path))
        suggestion = _get_suggestion(error)
        error_messages.append(f"[{path}] {error.message}\n  -> {suggestion}")

    full_message = "Configuration validation failed:\n" + "\n".join(error_messages)
    raise ApiForgeConfigError(full_message)


def _validate_config_fallback(config: dict[str, Any]) -> None:
    """Fallback validation when schema is not available."""
    if "base_url" not in config:
        raise ApiForgeConfigError("Config must contain 'base_url'")

    if "resources" not in config:
        raise ApiForgeConfigError("Config must contain 'resources'")

    if not isinstance(config["resources"], dict):
        raise ApiForgeConfigError("'resources' must be a dictionary")

    for name, resource in config["resources"].items():
        if "path" not in resource:
            raise ApiForgeConfigError(f"Resource '{name}' must contain 'path'")


def get_config_path(provider: str, api_name: str) -> Path:
    """Get the default config path for a provider/API.

    Args:
        provider: Provider name (e.g., 'yandex')
        api_name: API name (e.g., 'metrika')

    Returns:
        Path to the config file
    """
    config_dir = Path.home() / ".apiforge" / "configs"
    return config_dir / provider / f"{api_name}.json"


def list_configs() -> dict[str, list[str]]:
    """List all available configs.

    Returns:
        Dictionary mapping provider names to lists of API names
    """
    config_dir = Path.home() / ".apiforge" / "configs"
    configs: dict[str, list[str]] = {}

    if not config_dir.exists():
        return configs

    for provider_dir in config_dir.iterdir():
        if provider_dir.is_dir():
            api_names = []
            for config_file in provider_dir.glob("*.json"):
                api_names.append(config_file.stem)
            if api_names:
                configs[provider_dir.name] = sorted(api_names)

    return configs
