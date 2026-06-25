"""Base adapter for ApiForge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..response import Response


class BaseAdapter(ABC):
    """Abstract base class for HTTP adapters."""

    def __init__(self, on_before_request: Optional[Any] = None) -> None:
        self._on_before_request = on_before_request

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send an HTTP request."""
        pass

    def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a GET request."""
        return self.request("GET", url, params=params, headers=headers, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
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
    ) -> Response:
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
    ) -> Response:
        """Send a DELETE request."""
        return self.request("DELETE", url, params=params, headers=headers, **kwargs)

    def patch(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a PATCH request."""
        return self.request(
            "PATCH", url, data=data, params=params, headers=headers, **kwargs
        )
