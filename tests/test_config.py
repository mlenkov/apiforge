"""Tests for config module."""

import json
import tempfile
from pathlib import Path

import pytest

from apiforge.config import (
    load_config,
    list_configs,
    get_config_path,
    _format_error_path,
    _get_suggestion,
    _validate_config,
)
from apiforge.exceptions import ApiForgeConfigError


class TestLoadConfig:
    def test_load_valid_config(self):
        config = {
            "base_url": "https://api.example.com",
            "resources": {
                "test": {"path": "/test"}
            },
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            f.flush()
            loaded = load_config(f.name)

        assert loaded["base_url"] == "https://api.example.com"

    def test_load_nonexistent_file(self):
        with pytest.raises(ApiForgeConfigError):
            load_config("/nonexistent/path.json")

    def test_load_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json")
            f.flush()
            with pytest.raises(ApiForgeConfigError):
                load_config(f.name)

    def test_load_wrong_format(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("test: value")
            f.flush()
            with pytest.raises(ApiForgeConfigError):
                load_config(f.name)

    def test_load_missing_base_url(self):
        config = {"resources": {"test": {"path": "/test"}}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            f.flush()
            with pytest.raises(ApiForgeConfigError):
                load_config(f.name)

    def test_load_missing_resources(self):
        config = {"base_url": "https://api.example.com"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            f.flush()
            with pytest.raises(ApiForgeConfigError):
                load_config(f.name)


class TestJsonSchemaValidation:
    def test_valid_config_with_all_fields(self):
        config = {
            "base_url": "https://api.example.com",
            "auth": {"token": "abc123"},
            "default_headers": {"X-Custom": "value"},
            "resources": {
                "users": {
                    "path": "/users/{id}",
                    "method": "GET",
                    "description": "Get user",
                    "parameters": {
                        "id": {"type": "string", "required": True}
                    },
                }
            },
        }
        _validate_config(config)

    def test_invalid_method_enum(self):
        config = {
            "base_url": "https://api.example.com",
            "resources": {
                "test": {"path": "/test", "method": "INVALID"}
            },
        }
        with pytest.raises(ApiForgeConfigError) as exc_info:
            _validate_config(config)
        assert "INVALID" in str(exc_info.value) or "enum" in str(exc_info.value).lower()

    def test_invalid_base_url_format(self):
        config = {
            "base_url": "not-a-uri",
            "resources": {"test": {"path": "/test"}},
        }
        with pytest.raises(ApiForgeConfigError) as exc_info:
            _validate_config(config)
        assert "format" in str(exc_info.value).lower() or "uri" in str(exc_info.value).lower()

    def test_wrong_type_for_method(self):
        config = {
            "base_url": "https://api.example.com",
            "resources": {
                "test": {"path": "/test", "method": 123}
            },
        }
        with pytest.raises(ApiForgeConfigError) as exc_info:
            _validate_config(config)
        assert "type" in str(exc_info.value).lower()

    def test_multiple_errors_reported(self):
        config = {
            "base_url": "https://api.example.com",
            "resources": {
                "test": {
                    "path": "/test",
                    "method": "INVALID",
                },
                "test2": {
                    "path": "/test2",
                    "method": "ALSO_INVALID",
                },
            },
        }
        with pytest.raises(ApiForgeConfigError) as exc_info:
            _validate_config(config)
        error_msg = str(exc_info.value)
        assert "Configuration validation failed" in error_msg


class TestErrorPathFormatting:
    def test_empty_path(self):
        assert _format_error_path([]) == "root"

    def test_single_key(self):
        assert _format_error_path(["base_url"]) == "base_url"

    def test_nested_path(self):
        assert _format_error_path(["resources", "users", "method"]) == "resources.users.method"

    def test_array_index(self):
        assert _format_error_path(["items", 0, "name"]) == "items[0].name"


class TestErrorSuggestions:
    def test_required_field_suggestion(self):
        config = {"resources": {"test": {"path": "/test"}}}
        with pytest.raises(ApiForgeConfigError) as exc_info:
            _validate_config(config)
        assert "Add" in str(exc_info.value) or "base_url" in str(exc_info.value)

    def test_method_suggestion(self):
        config = {
            "base_url": "https://api.example.com",
            "resources": {"test": {"path": "/test", "method": "GET"}},
        }
        _validate_config(config)


class TestGetConfigPath:
    def test_get_config_path(self):
        path = get_config_path("yandex", "metrika")
        assert path.name == "metrika.json"
        assert "yandex" in str(path)


class TestListConfigs:
    def test_list_configs_empty(self, tmp_path):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.MonkeyPatch.context() as m:
                m.setenv("HOME", tmpdir)
                configs = list_configs()
                assert configs == {}


class TestGetConfigPath:
    def test_get_config_path(self):
        path = get_config_path("yandex", "metrika")
        assert path.name == "metrika.json"
        assert "yandex" in str(path)


class TestListConfigs:
    def test_list_configs_empty(self, tmp_path):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.MonkeyPatch.context() as m:
                m.setenv("HOME", tmpdir)
                configs = list_configs()
                assert configs == {}
