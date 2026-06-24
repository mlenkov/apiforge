"""Resource module for ApiForge."""

from __future__ import annotations

from typing import Any, Optional


class Resource:
    """Represents an API resource/endpoint."""

    def __init__(
        self,
        name: str,
        path: str,
        method: str = "GET",
        description: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.name = name
        self.path = path
        self.method = method.upper()
        self.description = description
        self.parameters = parameters or {}
        self.headers = headers or {}

    def __repr__(self) -> str:
        return f"Resource(name={self.name!r}, path={self.path!r}, method={self.method!r})"

    def build_url(self, base_url: str, **kwargs: Any) -> str:
        """Build the full URL for this resource."""
        path = self.path.format(**kwargs)
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_required_params(self) -> list[str]:
        """Get list of required parameter names."""
        return [
            name
            for name, config in self.parameters.items()
            if config.get("required", False)
        ]

    def validate_params(self, params: dict[str, Any]) -> list[str]:
        """Validate parameters against resource definition.

        Returns list of missing required parameters.
        """
        required = self.get_required_params()
        return [p for p in required if p not in params]
