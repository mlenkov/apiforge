"""Executor module for ApiForge."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .response import Response

if TYPE_CHECKING:
    from .adapters.base import BaseAdapter


class Executor:
    """Coordinates HTTP execution using an adapter as transport."""

    def __init__(
        self,
        base_url: str = "",
        auth: Optional[dict[str, str]] = None,
        default_headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        adapter: Optional[BaseAdapter] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.auth = auth or {}
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._adapter = adapter

    def _get_adapter(self) -> BaseAdapter:
        """Get or create the default HTTP adapter."""
        if self._adapter is None:
            from .adapters.requests_adapter import RequestsAdapter

            self._adapter = RequestsAdapter(
                base_url=self.base_url,
                auth=self.auth or None,
                default_headers=self.default_headers,
                timeout=self.timeout,
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
            )
        return self._adapter

    def execute(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Execute an HTTP request via the adapter."""
        adapter = self._get_adapter()
        return adapter.request(
            method=method,
            url=path,
            params=params,
            data=data,
            headers=headers,
            **kwargs,
        )

    def close(self) -> None:
        """Close the adapter if it has a close method."""
        if self._adapter is not None and hasattr(self._adapter, "close"):
            self._adapter.close()

    def __enter__(self) -> Executor:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
