"""Config loader module for ApiForge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..exceptions import ApiForgeConfigError
from .validator import validate_config


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

    validate_config(config)
    return config
