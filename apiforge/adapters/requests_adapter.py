"""Requests-based HTTP adapter for ApiForge."""

from __future__ import annotations

import time
from typing import Any, Callable, Optional

import requests

from ..core.response import Response
from ..exceptions import (
    ApiForgeAuthenticationError,
    ApiForgeRateLimitError,
    ApiForgeRequestError,
    ApiForgeResourceNotFoundError,
)
from .base import BaseAdapter


class RequestsAdapter(BaseAdapter):
    """HTTP adapter using the requests library."""

    def __init__(
        self,
        base_url: str = "",
        auth: Optional[dict[str, str]] = None,
        default_headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        on_before_request: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        super().__init__(on_before_request=on_before_request)
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()

    def _build_url(self, url: str) -> str:
        """Build full URL from base URL and relative path."""
        if self.base_url:
            return f"{self.base_url}/{url.lstrip('/')}"
        return url

    def _merge_headers(self, headers: Optional[dict[str, str]]) -> dict[str, str]:
        """Merge default headers with request-specific headers."""
        return {**self.default_headers, **(headers or {})}

    def request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send an HTTP request with retry logic."""
        full_url = self._build_url(url)
        request_headers = self._merge_headers(headers)

        for attempt in range(self.max_retries + 1):
            if self._on_before_request is not None:
                self._on_before_request(method, full_url)

            try:
                response = self.session.request(
                    method=method,
                    url=full_url,
                    params=params,
                    json=data if data else None,
                    headers=request_headers,
                    timeout=self.timeout,
                    **kwargs,
                )

                if response.status_code == 401:
                    raise ApiForgeAuthenticationError(
                        "Authentication failed",
                        status_code=401,
                        response=response,
                    )

                if response.status_code == 404:
                    raise ApiForgeResourceNotFoundError(
                        "Resource not found",
                        status_code=404,
                        response=response,
                    )

                if response.status_code == 429:
                    retry_after = self._parse_retry_after(
                        response.headers.get("Retry-After"), self.retry_delay
                    )
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue
                    raise ApiForgeRateLimitError(
                        "Rate limit exceeded",
                        retry_after=retry_after,
                        response=response,
                    )

                if response.status_code >= 500 and attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue

                if response.status_code >= 400:
                    raise ApiForgeRequestError(
                        f"Request failed: {response.status_code}",
                        status_code=response.status_code,
                        response=response,
                    )

                return Response(
                    status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers),
                )

            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise ApiForgeRequestError(
                    f"Connection error: {e}",
                    response=None,
                ) from e

            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise ApiForgeRequestError(
                    f"Request timeout: {e}",
                    response=None,
                ) from e

        raise ApiForgeRequestError("Max retries exceeded")

    @staticmethod
    def _parse_retry_after(value: Optional[str], default: float) -> float:
        """Parse Retry-After header, falling back to default."""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self) -> RequestsAdapter:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
