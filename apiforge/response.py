"""Response module for ApiForge."""

from __future__ import annotations

import json
from typing import Any, Optional


class Response:
    """Wrapper for API responses."""

    def __init__(
        self,
        status_code: int,
        content: bytes,
        headers: dict[str, str],
        data: Optional[Any] = None,
    ) -> None:
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self._data = data

    @property
    def data(self) -> Any:
        """Parse and return response data."""
        if self._data is not None:
            return self._data

        if not self.content:
            return None

        content_type = self.headers.get("content-type", "")
        if "json" in content_type:
            return json.loads(self.content)
        try:
            return self.content.decode("utf-8")
        except UnicodeDecodeError:
            return self.content.decode("latin-1")

    @property
    def ok(self) -> bool:
        """Check if response status is 2xx."""
        return 200 <= self.status_code < 300

    def json(self) -> Any:
        """Parse response as JSON."""
        if not self.content:
            return None
        return json.loads(self.content)

    def text(self) -> str:
        """Return response as text."""
        try:
            return self.content.decode("utf-8")
        except UnicodeDecodeError:
            return self.content.decode("latin-1")

    def __repr__(self) -> str:
        return f"Response(status_code={self.status_code})"
