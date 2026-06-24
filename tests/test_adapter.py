"""Tests for HTTP adapter and executor architecture."""

from unittest.mock import MagicMock, patch, PropertyMock

import pytest
import requests

from apiforge.adapters.http import HTTPAdapter
from apiforge.core.executor import ApiForgeExecutor
from apiforge.core.client import ApiForgeClient
from apiforge.core.response import ApiForgeResponse
from apiforge.exceptions import (
    ApiForgeAuthenticationError,
    ApiForgeRateLimitError,
    ApiForgeRequestError,
    ApiForgeResourceNotFoundError,
)


@pytest.fixture
def sample_config():
    return {
        "base_url": "https://api.example.com",
        "auth": {"token": "test_token"},
        "resources": {
            "get_users": {
                "path": "/users",
                "method": "GET",
                "description": "Get all users",
            },
        },
    }


class TestHTTPAdapter:
    def test_adapter_creation(self):
        adapter = HTTPAdapter(
            base_url="https://api.example.com",
            auth={"token": "test"},
            default_headers={"X-Custom": "value"},
            timeout=10.0,
            max_retries=5,
            retry_delay=2.0,
        )
        assert adapter.base_url == "https://api.example.com"
        assert adapter.auth == {"token": "test"}
        assert adapter.default_headers == {"X-Custom": "value"}
        assert adapter.timeout == 10.0
        assert adapter.max_retries == 5
        assert adapter.retry_delay == 2.0

    def test_adapter_context_manager(self):
        with HTTPAdapter(base_url="https://api.example.com") as adapter:
            assert adapter is not None
            assert adapter.session is not None

    def test_build_url_with_base(self):
        adapter = HTTPAdapter(base_url="https://api.example.com")
        url = adapter._build_url("/users")
        assert url == "https://api.example.com/users"

    def test_build_url_without_base(self):
        adapter = HTTPAdapter()
        url = adapter._build_url("https://other.com/users")
        assert url == "https://other.com/users"

    def test_merge_headers(self):
        adapter = HTTPAdapter(
            base_url="",
            default_headers={"X-Default": "value"},
        )
        merged = adapter._merge_headers({"X-Custom": "custom"})
        assert merged == {"X-Default": "value", "X-Custom": "custom"}

    @patch("requests.Session.request")
    def test_request_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"ok": true}'
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(base_url="https://api.example.com")
        response = adapter.request("GET", "/users")

        assert response.status_code == 200
        assert response.content == b'{"ok": true}'

    @patch("requests.Session.request")
    def test_request_401_raises_auth_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = b'Unauthorized'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(base_url="https://api.example.com")
        with pytest.raises(ApiForgeAuthenticationError):
            adapter.request("GET", "/users")

    @patch("requests.Session.request")
    def test_request_404_raises_not_found(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b'Not Found'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(base_url="https://api.example.com")
        with pytest.raises(ApiForgeResourceNotFoundError):
            adapter.request("GET", "/missing")

    @patch("requests.Session.request")
    def test_request_429_retries_then_raises(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.content = b'Rate limited'
        mock_response.headers = {"Retry-After": "0.01"}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(base_url="https://api.example.com", max_retries=2)
        with pytest.raises(ApiForgeRateLimitError):
            adapter.request("GET", "/users")

        assert mock_request.call_count == 3

    @patch("requests.Session.request")
    def test_request_5xx_retries_then_raises(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b'Server error'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(
            base_url="https://api.example.com",
            max_retries=2,
            retry_delay=0.01,
        )
        with pytest.raises(ApiForgeRequestError):
            adapter.request("GET", "/users")

        assert mock_request.call_count == 3

    @patch("requests.Session.request")
    def test_request_connection_error_retries(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError("Conn error")

        adapter = HTTPAdapter(
            base_url="https://api.example.com",
            max_retries=2,
            retry_delay=0.01,
        )
        with pytest.raises(ApiForgeRequestError, match="Connection error"):
            adapter.request("GET", "/users")

        assert mock_request.call_count == 3

    @patch("requests.Session.request")
    def test_request_timeout_retries(self, mock_request):
        mock_request.side_effect = requests.exceptions.Timeout("Timed out")

        adapter = HTTPAdapter(
            base_url="https://api.example.com",
            max_retries=2,
            retry_delay=0.01,
        )
        with pytest.raises(ApiForgeRequestError, match="timeout"):
            adapter.request("GET", "/users")

        assert mock_request.call_count == 3

    @patch("requests.Session.request")
    def test_request_400_raises_immediately(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.content = b'Bad request'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        adapter = HTTPAdapter(base_url="https://api.example.com", max_retries=3)
        with pytest.raises(ApiForgeRequestError):
            adapter.request("GET", "/users")

        assert mock_request.call_count == 1

    def test_close(self):
        adapter = HTTPAdapter()
        adapter.close()

    def test_get_convenience(self):
        adapter = HTTPAdapter(base_url="https://api.example.com")
        with patch.object(adapter, "request") as mock_request:
            mock_request.return_value = ApiForgeResponse(200, b"ok", {})
            adapter.get("/users", params={"limit": "10"})
            mock_request.assert_called_once_with(
                "GET", "/users", params={"limit": "10"}, headers=None
            )

    def test_post_convenience(self):
        adapter = HTTPAdapter(base_url="https://api.example.com")
        with patch.object(adapter, "request") as mock_request:
            mock_request.return_value = ApiForgeResponse(201, b"created", {})
            adapter.post("/users", data={"name": "test"})
            mock_request.assert_called_once_with(
                "POST", "/users", data={"name": "test"}, params=None, headers=None
            )


class TestApiForgeExecutor:
    def test_executor_with_adapter(self):
        mock_adapter = MagicMock()
        mock_adapter.request.return_value = ApiForgeResponse(200, b"ok", {})

        executor = ApiForgeExecutor(
            base_url="https://api.example.com",
            adapter=mock_adapter,
        )

        response = executor.execute("GET", "/users")

        assert response.status_code == 200
        mock_adapter.request.assert_called_once_with(
            method="GET",
            url="/users",
            params=None,
            data=None,
            headers=None,
        )

    def test_executor_lazy_adapter_creation(self):
        executor = ApiForgeExecutor(
            base_url="https://api.example.com",
            max_retries=5,
            timeout=10.0,
        )

        adapter = executor._get_adapter()
        assert isinstance(adapter, HTTPAdapter)
        assert adapter.base_url == "https://api.example.com"
        assert adapter.max_retries == 5
        assert adapter.timeout == 10.0

    def test_executor_context_manager(self):
        with ApiForgeExecutor(base_url="https://api.example.com") as executor:
            assert executor is not None

    def test_executor_close(self):
        executor = ApiForgeExecutor(base_url="https://api.example.com")
        executor._get_adapter()
        executor.close()

    def test_executor_custom_adapter_not_overwritten(self):
        mock_adapter = MagicMock()
        executor = ApiForgeExecutor(adapter=mock_adapter)
        adapter = executor._get_adapter()
        assert adapter is mock_adapter

    @patch("requests.Session.request")
    def test_executor_full_flow(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response

        executor = ApiForgeExecutor(
            base_url="https://api.example.com",
            max_retries=1,
            timeout=5.0,
        )
        response = executor.execute("GET", "/test", params={"q": "1"})

        assert response.status_code == 200
        mock_request.assert_called_once()


class TestClientWithAdapter:
    def test_client_creates_adapter(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        assert hasattr(client, "_adapter")
        assert isinstance(client._adapter, HTTPAdapter)

    def test_client_context_manager(self, sample_config):
        with ApiForgeClient(config=sample_config) as client:
            assert client is not None
            assert hasattr(client, "_adapter")

    @patch("requests.Session.request")
    def test_client_request_uses_adapter(self, mock_request, sample_config):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"users": []}'
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response

        client = ApiForgeClient(config=sample_config)
        response = client.request("get_users")

        assert response.status_code == 200
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_client_adapter_retries(self, mock_request, sample_config):
        fail_response = MagicMock()
        fail_response.status_code = 500
        fail_response.content = b'Error'
        fail_response.headers = {}

        ok_response = MagicMock()
        ok_response.status_code = 200
        ok_response.content = b'{"ok": true}'
        ok_response.headers = {"content-type": "application/json"}

        mock_request.side_effect = [fail_response, ok_response]

        client = ApiForgeClient(config=sample_config)
        response = client.request("get_users")

        assert response.status_code == 200
        assert mock_request.call_count == 2
