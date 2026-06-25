"""Backward-compat shim — use apiforge.config package instead."""

from .config import get_config_path, list_configs, load_config, validate_config
from .config.validator import (
    _format_error_path,
    _get_suggestion,
    _validate_config,
)

__all__ = [
    "load_config",
    "validate_config",
    "get_config_path",
    "list_configs",
    "_format_error_path",
    "_get_suggestion",
    "_validate_config",
]
