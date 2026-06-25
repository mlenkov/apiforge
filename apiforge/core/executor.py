"""Backward-compat shim — use apiforge.executor.Executor instead."""

from ...executor import Executor as ApiForgeExecutor

__all__ = ["ApiForgeExecutor"]
