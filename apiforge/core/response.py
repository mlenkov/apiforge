"""Backward-compat shim — use apiforge.response.Response instead."""

from ...response import Response as ApiForgeResponse

__all__ = ["ApiForgeResponse"]
