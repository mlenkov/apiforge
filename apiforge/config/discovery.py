"""Config discovery module for ApiForge."""

from __future__ import annotations

from pathlib import Path
from typing import Any


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
            api_names: list[str] = []
            for config_file in provider_dir.glob("*.json"):
                api_names.append(config_file.stem)
            if api_names:
                configs[provider_dir.name] = sorted(api_names)

    return configs
