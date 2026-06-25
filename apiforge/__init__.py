"""ApiForge - Modern Python API Client Generator."""

__version__ = "0.1.0"
__author__ = "ApiForge Contributors"

from .client import Client
from .config import get_config_path, list_configs, load_config, validate_config
from .exceptions import (
    ApiForgeAuthenticationError,
    ApiForgeConfigError,
    ApiForgeError,
    ApiForgeRateLimitError,
    ApiForgeRequestError,
    ApiForgeResourceNotFoundError,
    ApiForgeResponseProcessError,
    ApiForgeValidationError,
)
from .resource import Resource
from .response import Response

# Backward-compatible aliases
ApiForgeClient = Client
ApiForgeResponse = Response
ApiForgeExecutor = None  # lazy import to avoid circular

__all__ = [
    # Primary exports
    "Client",
    "Resource",
    "Response",
    # Config
    "load_config",
    "validate_config",
    "get_config_path",
    "list_configs",
    # Exceptions
    "ApiForgeError",
    "ApiForgeRequestError",
    "ApiForgeValidationError",
    "ApiForgeAuthenticationError",
    "ApiForgeRateLimitError",
    "ApiForgeResourceNotFoundError",
    "ApiForgeResponseProcessError",
    "ApiForgeConfigError",
    # Backward-compatible aliases
    "ApiForgeClient",
    "ApiForgeResponse",
]
