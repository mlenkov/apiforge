"""Base serializer for ApiForge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """Abstract base class for serializers."""

    @abstractmethod
    def dumps(self, data: Any) -> str | bytes:
        """Serialize data to string/bytes."""
        pass

    @abstractmethod
    def loads(self, data: str | bytes) -> Any:
        """Deserialize string/bytes to data."""
        pass
