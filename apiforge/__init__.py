"""ApiForge - Modern Python API Client Generator"""

__version__ = "0.1.0"
__author__ = "ApiForge Contributors"

from .core.client import ApiForgeClient
from .core.resource import Resource
from .core.response import ApiForgeResponse

__all__ = ["ApiForgeClient", "Resource", "ApiForgeResponse"]
