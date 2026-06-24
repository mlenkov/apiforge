"""Client module for ApiForge."""

from __future__ import annotations

from typing import Any, Optional

from ..adapters.http import HTTPAdapter
from ..config import load_config
from ..exceptions import ApiForgeConfigError
from .executor import ApiForgeExecutor
from .resource import Resource
from .response import ApiForgeResponse


class ApiForgeClient:
    """Main client for ApiForge API interactions."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
        auth: Optional[dict[str, str]] = None,
        base_url: Optional[str] = None,
        default_headers: Optional[dict[str, str]] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize ApiForgeClient.

        Args:
            config_path: Path to JSON config file
            config: Config dict (alternative to config_path)
            auth: Authentication credentials
            base_url: Override base URL from config
            default_headers: Default headers for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        if config_path:
            self._config = load_config(config_path)
        elif config:
            self._config = config
        else:
            raise ApiForgeConfigError(
                "Either config_path or config must be provided"
            )

        self._base_url = base_url or self._config.get("base_url", "")
        self._auth = auth or self._config.get("auth", {})
        self._default_headers = {
            **self._config.get("default_headers", {}),
            **(default_headers or {}),
        }

        self._adapter = HTTPAdapter(
            base_url=self._base_url,
            auth=self._auth or None,
            default_headers=self._default_headers,
            timeout=timeout,
            max_retries=max_retries,
        )

        self._executor = ApiForgeExecutor(
            base_url=self._base_url,
            auth=self._auth,
            default_headers=self._default_headers,
            timeout=timeout,
            max_retries=max_retries,
            adapter=self._adapter,
        )

        self._resources: dict[str, Resource] = {}
        self._load_resources()

    def _load_resources(self) -> None:
        """Load resources from config."""
        resources_config = self._config.get("resources", {})
        for name, res_config in resources_config.items():
            self._resources[name] = Resource(
                name=name,
                path=res_config["path"],
                method=res_config.get("method", "GET"),
                description=res_config.get("description"),
                parameters=res_config.get("parameters", {}),
                headers=res_config.get("headers", {}),
            )

    def get_resource(self, name: str) -> Resource:
        """Get a resource by name."""
        if name not in self._resources:
            raise ApiForgeConfigError(f"Resource '{name}' not found in config")
        return self._resources[name]

    def list_resources(self) -> list[str]:
        """List all available resource names."""
        return list(self._resources.keys())

    def request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a request using a named resource.

        Args:
            resource_name: Name of the resource to use
            params: Query parameters
            data: Request body data
            **kwargs: Additional arguments for path formatting

        Returns:
            ApiForgeResponse object
        """
        resource = self.get_resource(resource_name)

        missing = resource.validate_params(params or {})
        if missing:
            raise ApiForgeConfigError(
                f"Missing required parameters: {', '.join(missing)}"
            )

        url = resource.build_url(self._base_url, **kwargs)

        return self._executor.execute(
            method=resource.method,
            path=resource.path.format(**kwargs),
            params=params,
            data=data,
            headers=resource.headers,
        )

    def get(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a GET request."""
        resource = self.get_resource(resource_name)
        resource.method = "GET"
        return self.request(resource_name, params=params, **kwargs)

    def post(
        self,
        resource_name: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a POST request."""
        resource = self.get_resource(resource_name)
        resource.method = "POST"
        return self.request(resource_name, params=params, data=data, **kwargs)

    def put(
        self,
        resource_name: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a PUT request."""
        resource = self.get_resource(resource_name)
        resource.method = "PUT"
        return self.request(resource_name, params=params, data=data, **kwargs)

    def delete(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a DELETE request."""
        resource = self.get_resource(resource_name)
        resource.method = "DELETE"
        return self.request(resource_name, params=params, **kwargs)

    def patch(
        self,
        resource_name: str,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiForgeResponse:
        """Make a PATCH request."""
        resource = self.get_resource(resource_name)
        resource.method = "PATCH"
        return self.request(resource_name, params=params, data=data, **kwargs)

    def close(self) -> None:
        """Close the adapter session."""
        self._adapter.close()

    def __enter__(self) -> ApiForgeClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
