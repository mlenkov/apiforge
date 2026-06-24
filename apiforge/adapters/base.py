"""Base adapter for ApiForge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..core.response import ApiForgeResponse


class BaseAdapter(ABC):
    """Abstract base class for HTTP adapters."""

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send an HTTP request."""
        pass

    def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send a GET request."""
        return self.request("GET", url, params=params, headers=headers, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send a POST request."""
        return self.request(
            "POST", url, data=data, params=params, headers=headers, **kwargs
        )

    def put(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send a PUT request."""
        return self.request(
            "PUT", url, data=data, params=params, headers=headers, **kwargs
        )

    def delete(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send a DELETE request."""
        return self.request("DELETE", url, params=params, headers=headers, **kwargs)

    def patch(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Send a PATCH request."""
        return self.request(
            "PATCH", url, data=data, params=params, headers=headers, **kwargs
        )
