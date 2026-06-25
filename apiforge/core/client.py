"""Backward-compat shim — use apiforge.client.Client instead."""

from ...client import Client as ApiForgeClient

__all__ = ["ApiForgeClient"]
