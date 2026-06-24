"""JSON serializer for ApiForge."""

from __future__ import annotations

import json
from typing import Any

from .base import BaseSerializer


class JSONSerializer(BaseSerializer):
    """JSON serializer using stdlib json."""

    def __init__(
        self,
        indent: int | None = None,
        ensure_ascii: bool = True,
        sort_keys: bool = False,
    ) -> None:
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.sort_keys = sort_keys

    def dumps(self, data: Any) -> str:
        """Serialize data to JSON string."""
        return json.dumps(
            data,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii,
            sort_keys=self.sort_keys,
        )

    def loads(self, data: str | bytes) -> Any:
        """Deserialize JSON string to data."""
        return json.loads(data)
