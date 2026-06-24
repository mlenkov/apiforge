"""Exceptions for ApiForge."""

from __future__ import annotations

from typing import Any, Optional


class ApiForgeError(Exception):
    """Base exception for ApiForge."""

    def __init__(
        self,
        message: str,
        response: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response = response
        self.data = data


class ApiForgeRequestError(ApiForgeError):
    """Exception raised for HTTP request errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(message, response, data)
        self.status_code = status_code


class ApiForgeValidationError(ApiForgeError):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str,
        errors: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(message, data=data)
        self.errors = errors or {}


class ApiForgeAuthenticationError(ApiForgeRequestError):
    """Exception raised for authentication errors."""

    pass


class ApiForgeRateLimitError(ApiForgeRequestError):
    """Exception raised for rate limit errors."""

    def __init__(
        self,
        message: str,
        retry_after: Optional[float] = None,
        response: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(message, response=response, data=data)
        self.retry_after = retry_after


class ApiForgeResourceNotFoundError(ApiForgeRequestError):
    """Exception raised when resource is not found."""

    pass


class ApiForgeResponseProcessError(ApiForgeError):
    """Exception raised when response processing fails."""

    pass


class ApiForgeConfigError(ApiForgeError):
    """Exception raised for configuration errors."""

    pass
