"""Tests for ApiForge client."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from apiforge import ApiForgeClient, ApiForgeResponse, Resource
from apiforge.config import load_config
from apiforge.exceptions import (
    ApiForgeConfigError,
    ApiForgeRequestError,
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
                "parameters": {
                    "limit": {"type": "integer", "required": False},
                    "offset": {"type": "integer", "required": False},
                },
            },
            "get_user": {
                "path": "/users/{user_id}",
                "method": "GET",
                "description": "Get user by ID",
                "parameters": {
                    "user_id": {"type": "string", "required": True},
                },
            },
            "create_user": {
                "path": "/users",
                "method": "POST",
                "description": "Create a new user",
                "parameters": {
                    "name": {"type": "string", "required": True},
                    "email": {"type": "string", "required": True},
                },
            },
        },
    }


@pytest.fixture
def config_file(sample_config):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample_config, f)
        return f.name


class TestResource:
    def test_resource_creation(self):
        resource = Resource(
            name="test",
            path="/test",
            method="GET",
            description="Test resource",
        )
        assert resource.name == "test"
        assert resource.path == "/test"
        assert resource.method == "GET"
        assert resource.description == "Test resource"

    def test_resource_repr(self):
        resource = Resource(name="test", path="/test", method="GET")
        assert "Resource(name='test'" in repr(resource)

    def test_build_url(self):
        resource = Resource(name="test", path="/users/{user_id}", method="GET")
        url = resource.build_url("https://api.example.com", user_id="123")
        assert url == "https://api.example.com/users/123"

    def test_get_required_params(self):
        resource = Resource(
            name="test",
            path="/test",
            parameters={
                "required_param": {"required": True},
                "optional_param": {"required": False},
            },
        )
        required = resource.get_required_params()
        assert "required_param" in required
        assert "optional_param" not in required

    def test_validate_params(self):
        resource = Resource(
            name="test",
            path="/test",
            parameters={
                "required_param": {"required": True},
                "optional_param": {"required": False},
            },
        )
        missing = resource.validate_params({"optional_param": "value"})
        assert "required_param" in missing


class TestApiForgeResponse:
    def test_response_creation(self):
        response = ApiForgeResponse(
            status_code=200,
            content=b'{"key": "value"}',
            headers={"content-type": "application/json"},
        )
        assert response.status_code == 200
        assert response.ok is True

    def test_response_json(self):
        response = ApiForgeResponse(
            status_code=200,
            content=b'{"key": "value"}',
            headers={"content-type": "application/json"},
        )
        data = response.json()
        assert data == {"key": "value"}

    def test_response_text(self):
        response = ApiForgeResponse(
            status_code=200,
            content=b"Hello, World!",
            headers={},
        )
        assert response.text() == "Hello, World!"

    def test_response_not_ok(self):
        response = ApiForgeResponse(
            status_code=404,
            content=b"Not Found",
            headers={},
        )
        assert response.ok is False


class TestApiForgeClient:
    def test_client_creation(self, config_file):
        client = ApiForgeClient(config_path=config_file)
        assert client._base_url == "https://api.example.com"

    def test_client_with_dict_config(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        assert client._base_url == "https://api.example.com"

    def test_client_no_config(self):
        with pytest.raises(ApiForgeConfigError):
            ApiForgeClient()

    def test_list_resources(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        resources = client.list_resources()
        assert "get_users" in resources
        assert "get_user" in resources
        assert "create_user" in resources

    def test_get_resource(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        resource = client.get_resource("get_users")
        assert resource.name == "get_users"
        assert resource.path == "/users"

    def test_get_resource_not_found(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        with pytest.raises(ApiForgeConfigError):
            client.get_resource("nonexistent")

    @patch("requests.Session.request")
    def test_request(self, mock_request, sample_config):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"users": []}'
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response

        client = ApiForgeClient(config=sample_config)
        response = client.request("get_users", params={"limit": 10})

        assert response.status_code == 200
        mock_request.assert_called_once()

    def test_request_missing_params(self, sample_config):
        client = ApiForgeClient(config=sample_config)
        with pytest.raises(ApiForgeConfigError):
            client.request("get_user")
