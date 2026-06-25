"""Core module for ApiForge — backward-compat shim."""

from ..client import Client as ApiForgeClient
from ..executor import Executor as ApiForgeExecutor
from ..resource import Resource
from ..response import Response as ApiForgeResponse

__all__ = ["ApiForgeClient", "ApiForgeExecutor", "Resource", "ApiForgeResponse"]
