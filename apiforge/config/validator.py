"""Config validator module for ApiForge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft7Validator, ValidationError

from ..exceptions import ApiForgeConfigError


def _get_schema() -> dict[str, Any]:
    """Load JSON Schema from template."""
    schema_path = Path.home() / ".apiforge" / "configs" / "_template" / "api_template.json"
    if not schema_path.exists():
        schema_path = (
            Path(__file__).parent.parent.parent
            / "examples"
            / "configs"
            / "_template"
            / "api_template.json"
        )
    if not schema_path.exists():
        raise ApiForgeConfigError("Cannot find schema template file")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _format_error_path(path: list[str | int]) -> str:
    """Format JSON Schema error path to human-readable string."""
    if not path:
        return "root"
    parts: list[str] = []
    for part in path:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def _get_suggestion(error: ValidationError) -> str:
    """Generate suggestion based on validation error."""
    path = _format_error_path(list(error.absolute_path))
    validator = error.validator

    if validator == "required":
        missing = error.message.split("'")[1] if "'" in error.message else "field"
        return f"Add '{missing}' to the configuration"

    if validator == "type":
        expected = error.message.split("'")[1] if "'" in error.message else "value"
        return f"Change '{path}' to be of type '{expected}'"

    if validator == "enum":
        allowed = (
            error.message.split("[")[1].split("]")[0]
            if "[" in error.message
            else "valid values"
        )
        return f"Use one of: {allowed}"

    if validator == "format":
        expected = (
            error.message.split("'")[1] if "'" in error.message else "valid format"
        )
        return f"Ensure '{path}' is a valid {expected}"

    if validator == "additionalProperties":
        return f"Remove unexpected property '{path}'"

    return "Check the configuration documentation"


def _validate_uri_format(config: dict[str, Any]) -> list[str]:
    """Validate URI format for base_url field."""
    errors: list[str] = []
    base_url = config.get("base_url")
    if base_url and not isinstance(base_url, str):
        return errors
    if base_url:
        try:
            result = urlparse(base_url)
            if not all([result.scheme, result.netloc]):
                errors.append(
                    "base_url must be a valid URI (e.g., https://api.example.com)"
                )
        except Exception:
            errors.append(
                "base_url must be a valid URI (e.g., https://api.example.com)"
            )
    return errors


def validate_config(config: dict[str, Any]) -> None:
    """Validate config using JSON Schema."""
    try:
        schema = _get_schema()
    except Exception:
        _validate_config_fallback(config)
        return

    validator = Draft7Validator(schema)
    errors: list[ValidationError] = list(validator.iter_errors(config))

    uri_errors = _validate_uri_format(config)
    for uri_err in uri_errors:
        errors.append(
            ValidationError(
                uri_err,
                validator="format",
                instance=config.get("base_url"),
                schema_path=["properties", "base_url", "format"],
            )
        )

    if not errors:
        return

    error_messages: list[str] = []
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
