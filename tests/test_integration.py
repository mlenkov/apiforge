"""Integration tests for ApiForge - full cycle: config -> client -> request -> response."""

import json
from unittest.mock import MagicMock, patch

import pytest

from apiforge import ApiForgeClient, ApiForgeResponse
from apiforge.serializers import JSONSerializer
from apiforge.exceptions import (
    ApiForgeConfigError,
    ApiForgeRequestError,
    ApiForgeAuthenticationError,
)


@pytest.fixture
def api_config():
    return {
        "base_url": "https://api.example.com",
        "auth": {"token": "test_token_123"},
        "default_headers": {"X-Client-Version": "1.0"},
        "resources": {
            "list_items": {
                "path": "/items",
                "method": "GET",
                "description": "List all items",
                "parameters": {
                    "limit": {"type": "integer", "required": False},
                    "offset": {"type": "integer", "required": False},
                },
            },
            "get_item": {
                "path": "/items/{item_id}",
                "method": "GET",
                "description": "Get item by ID",
                "parameters": {
                    "item_id": {"type": "string", "required": True},
                },
            },
            "create_item": {
                "path": "/items",
                "method": "POST",
                "description": "Create a new item",
                "parameters": {
                    "name": {"type": "string", "required": True},
                },
            },
            "update_item": {
                "path": "/items/{item_id}",
                "method": "PUT",
                "description": "Update an item",
                "parameters": {
                    "item_id": {"type": "string", "required": True},
                    "name": {"type": "string", "required": True},
                },
            },
            "delete_item": {
                "path": "/items/{item_id}",
                "method": "DELETE",
                "description": "Delete an item",
                "parameters": {
                    "item_id": {"type": "string", "required": True},
                },
            },
        },
    }


@pytest.fixture
def mock_http_response():
    def _make_response(status_code, data, headers=None):
        response = MagicMock()
        response.status_code = status_code
        response.content = json.dumps(data).encode("utf-8") if isinstance(data, dict) else data
        response.headers = headers or {"content-type": "application/json"}
        return response
    return _make_response


class TestConfigToClient:
    def test_config_creates_client(self, api_config):
        client = ApiForgeClient(config=api_config)

        assert client._base_url == "https://api.example.com"
        assert client._auth == {"token": "test_token_123"}
        assert "list_items" in client.list_resources()
        assert "get_item" in client.list_resources()
        assert "create_item" in client.list_resources()

    def test_client_lists_all_resources(self, api_config):
        client = ApiForgeClient(config=api_config)
        resources = client.list_resources()
        assert len(resources) == 5

    def test_client_gets_resource(self, api_config):
        client = ApiForgeClient(config=api_config)
        resource = client.get_resource("get_item")
        assert resource.path == "/items/{item_id}"
        assert resource.method == "GET"


class TestClientRequestFlow:
    @patch("requests.Session.request")
    def test_list_items(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {
            "items": [{"id": 1, "name": "Item 1"}],
            "total": 1,
        })

        client = ApiForgeClient(config=api_config)
        response = client.request("list_items", params={"limit": 10})

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_get_item_by_id(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {
            "id": "abc123",
            "name": "Test Item",
        })

        client = ApiForgeClient(config=api_config)
        response = client.request(
            "get_item",
            params={"item_id": "abc123"},
            item_id="abc123",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "abc123"
        assert data["name"] == "Test Item"

    @patch("requests.Session.request")
    def test_create_item(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(201, {
            "id": "new123",
            "name": "New Item",
        })

        client = ApiForgeClient(config=api_config)
        response = client.request(
            "create_item",
            params={"name": "New Item"},
            data={"name": "New Item"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "new123"

    @patch("requests.Session.request")
    def test_delete_item(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"deleted": True})

        client = ApiForgeClient(config=api_config)
        response = client.request(
            "delete_item",
            params={"item_id": "abc123"},
            item_id="abc123",
        )

        assert response.status_code == 200


class TestClientConvenienceMethods:
    @patch("requests.Session.request")
    def test_get_method(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"items": []})

        client = ApiForgeClient(config=api_config)
        response = client.get("list_items", params={"limit": 5})

        assert response.status_code == 200
        call_kwargs = mock_request.call_args
        assert call_kwargs[1]["method"] == "GET"

    @patch("requests.Session.request")
    def test_post_method(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(201, {"id": "new"})

        client = ApiForgeClient(config=api_config)
        response = client.post(
            "create_item",
            params={"name": "Item"},
            data={"name": "Item"},
        )

        assert response.status_code == 201

    @patch("requests.Session.request")
    def test_put_method(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"updated": True})

        client = ApiForgeClient(config=api_config)
        response = client.put(
            "update_item",
            params={"item_id": "abc", "name": "Updated"},
            data={"name": "Updated"},
            item_id="abc",
        )

        assert response.status_code == 200

    @patch("requests.Session.request")
    def test_delete_method(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"deleted": True})

        client = ApiForgeClient(config=api_config)
        response = client.delete(
            "delete_item",
            params={"item_id": "abc"},
            item_id="abc",
        )

        assert response.status_code == 200


class TestClientErrorHandling:
    @patch("requests.Session.request")
    def test_auth_error_propagates(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(401, {"error": "unauthorized"})

        client = ApiForgeClient(config=api_config)
        with pytest.raises(ApiForgeAuthenticationError):
            client.request("list_items")

    @patch("requests.Session.request")
    def test_server_error_with_retries(self, mock_request, api_config, mock_http_response):
        error_resp = mock_http_response(500, {"error": "server error"})
        ok_resp = mock_http_response(200, {"items": []})
        mock_request.side_effect = [error_resp, ok_resp]

        client = ApiForgeClient(config=api_config, max_retries=2)
        response = client.request("list_items")

        assert response.status_code == 200
        assert mock_request.call_count == 2

    def test_missing_required_params(self, api_config):
        client = ApiForgeClient(config=api_config)
        with pytest.raises(ApiForgeConfigError, match="Missing required parameters"):
            client.request("get_item")

    def test_nonexistent_resource(self, api_config):
        client = ApiForgeClient(config=api_config)
        with pytest.raises(ApiForgeConfigError, match="not found"):
            client.request("nonexistent_resource")


class TestResponseProcessing:
    @patch("requests.Session.request")
    def test_response_json_parsing(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"data": [1, 2, 3]})

        client = ApiForgeClient(config=api_config)
        response = client.request("list_items")

        assert response.ok
        data = response.json()
        assert data["data"] == [1, 2, 3]

    @patch("requests.Session.request")
    def test_response_text_parsing(self, mock_request, api_config):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"plain text response"
        mock_response.headers = {"content-type": "text/plain"}
        mock_request.return_value = mock_response

        client = ApiForgeClient(config=api_config)
        response = client.request("list_items")

        assert response.ok
        assert response.text() == "plain text response"

    @patch("requests.Session.request")
    def test_response_data_property(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"count": 42})

        client = ApiForgeClient(config=api_config)
        response = client.request("list_items")

        assert response.data == {"count": 42}

    @patch("requests.Session.request")
    def test_response_not_ok_raises_error(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(400, {"error": "bad request"})

        client = ApiForgeClient(config=api_config)
        with pytest.raises(ApiForgeRequestError, match="400"):
            client.request("list_items")


class TestSerializerIntegration:
    def test_json_serializer_with_client_data(self, api_config):
        s = JSONSerializer(indent=2)
        data = api_config["resources"]
        serialized = s.dumps(data)
        deserialized = s.loads(serialized)
        assert deserialized == data

    def test_serializer_roundtrip_with_response_data(self):
        s = JSONSerializer()
        response_data = {
            "status": "ok",
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
            ],
            "meta": {"total": 2, "page": 1},
        }
        serialized = s.dumps(response_data)
        deserialized = s.loads(serialized)
        assert deserialized == response_data


class TestClientContextManager:
    @patch("requests.Session.request")
    def test_client_as_context_manager(self, mock_request, api_config, mock_http_response):
        mock_request.return_value = mock_http_response(200, {"items": []})

        with ApiForgeClient(config=api_config) as client:
            response = client.request("list_items")
            assert response.status_code == 200

    def test_client_closes_session(self, api_config):
        client = ApiForgeClient(config=api_config)
        with patch.object(client._adapter, "close") as mock_close:
            client.close()
            mock_close.assert_called_once()
