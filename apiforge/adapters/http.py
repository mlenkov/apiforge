"""Backward-compat shim — use apiforge.adapters.requests_adapter.RequestsAdapter instead."""

from .requests_adapter import RequestsAdapter as HTTPAdapter

__all__ = ["HTTPAdapter"]
