"""Tests for Yandex Metrika configuration."""

import json
import os
import pytest
from pathlib import Path

from apiforge import ApiForgeClient
from apiforge.config import load_config


@pytest.fixture
def metrika_config_path():
    """Path to Yandex Metrika config file."""
    return Path(__file__).parent.parent / "configs" / "yandex" / "metrika.json"


@pytest.fixture
def metrika_config(metrika_config_path):
    """Load Yandex Metrika configuration."""
    return load_config(metrika_config_path)


class TestYandexMetrikaConfig:
    """Tests for Yandex Metrika configuration file."""
    
    def test_config_loads(self, metrika_config):
        """Test that config file loads successfully."""
        assert metrika_config is not None
        assert "base_url" in metrika_config
        assert "resources" in metrika_config
    
    def test_base_url(self, metrika_config):
        """Test base URL is correct."""
        assert metrika_config["base_url"] == "https://api-metrika.yandex.net"
    
    def test_auth_structure(self, metrika_config):
        """Test auth structure is correct."""
        assert "auth" in metrika_config
        assert "token" in metrika_config["auth"]
    
    def test_default_headers(self, metrika_config):
        """Test default headers are present."""
        assert "default_headers" in metrika_config
        headers = metrika_config["default_headers"]
        assert "Content-Type" in headers
    
    def test_management_resources(self, metrika_config):
        """Test management API resources exist."""
        resources = metrika_config["resources"]
        
        # Counters
        assert "counters" in resources
        assert "counter" in resources
        assert "counter_create" in resources
        assert "counter_update" in resources
        assert "counter_delete" in resources
        assert "counter_undelete" in resources
        
        # Goals
        assert "goals" in resources
        assert "goal" in resources
        assert "goal_create" in resources
        assert "goal_update" in resources
        assert "goal_delete" in resources
        
        # Filters
        assert "filters" in resources
        assert "filter_create" in resources
        assert "filter_delete" in resources
        
        # Operations
        assert "operations" in resources
        
        # Grants
        assert "grants" in resources
        assert "grant_create" in resources
        assert "grant_delete" in resources
        
        # Segments
        assert "segments" in resources
        assert "segment_create" in resources
        assert "segment_delete" in resources
        
        # Labels
        assert "labels" in resources
        assert "label_create" in resources
        assert "label_update" in resources
        assert "label_delete" in resources
        assert "label_bind_counters" in resources
        assert "label_unbind_counters" in resources
        
        # Accounts
        assert "accounts" in resources
        
        # Representatives
        assert "representatives" in resources
        assert "representative_create" in resources
        assert "representative_delete" in resources
        
        # Direct clients
        assert "direct_clients" in resources
        assert "direct_clients_bind" in resources
        assert "direct_clients_unbind" in resources
        
        # Exports
        assert "exports" in resources
        assert "export_create" in resources
        assert "export_delete" in resources
    
    def test_stat_resources(self, metrika_config):
        """Test statistics API resources exist."""
        resources = metrika_config["resources"]
        
        assert "stat_data" in resources
        assert "stat_data_drilldown" in resources
        assert "stat_data_bytime" in resources
        assert "stat_data_comparison" in resources
    
    def test_logs_resources(self, metrika_config):
        """Test logs API resources exist."""
        resources = metrika_config["resources"]
        
        assert "logrequests" in resources
        assert "logrequest" in resources
        assert "logrequest_create" in resources
        assert "logrequest_cancel" in resources
        assert "logrequest_reset" in resources
        assert "logrequest_clean" in resources
        assert "logrequest_download" in resources
    
    def test_reference_resources(self, metrika_config):
        """Test reference API resources exist."""
        resources = metrika_config["resources"]
        
        assert "messengers" in resources
        assert "social_networks" in resources
        assert "currencies" in resources
        assert "timezones" in resources
    
    def test_counters_parameters(self, metrika_config):
        """Test counters resource has parameters."""
        counters = metrika_config["resources"]["counters"]
        assert "parameters" in counters
        assert "per_page" in counters["parameters"]
        assert "offset" in counters["parameters"]
        assert "sort" in counters["parameters"]
    
    def test_stat_data_parameters(self, metrika_config):
        """Test stat_data resource has parameters."""
        stat_data = metrika_config["resources"]["stat_data"]
        assert "parameters" in stat_data
        assert "id" in stat_data["parameters"]
        assert "metrics" in stat_data["parameters"]
        assert "dimensions" in stat_data["parameters"]
        assert "date1" in stat_data["parameters"]
        assert "date2" in stat_data["parameters"]
        assert "limit" in stat_data["parameters"]
    
    def test_goal_types(self, metrika_config):
        """Test goal_create has correct type enum."""
        goal_create = metrika_config["resources"]["goal_create"]
        goal_param = goal_create["parameters"]["goal"]
        goal_type_param = goal_param["properties"]["type"]
        
        assert "enum" in goal_type_param
        expected_types = [
            "url", "action", "step", "number", "visit_duration",
            "file", "phone", "email", "messenger", "social", "chat", "payment_system"
        ]
        for goal_type in expected_types:
            assert goal_type in goal_type_param["enum"]


class TestYandexMetrikaClient:
    """Tests for Yandex Metrika client initialization."""
    
    def test_client_creation(self, metrika_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=metrika_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_all_resources(self, metrika_config):
        """Test client loads all resources from config."""
        client = ApiForgeClient(config=metrika_config)
        resources = client.list_resources()
        
        expected_resources = [
            "counters", "counter", "counter_create", "counter_update",
            "counter_delete", "counter_undelete",
            "goals", "goal", "goal_create", "goal_update", "goal_delete",
            "filters", "filter_create", "filter_delete",
            "operations",
            "grants", "grant_create", "grant_delete",
            "segments", "segment_create", "segment_delete",
            "labels", "label_create", "label_update", "label_delete",
            "label_bind_counters", "label_unbind_counters",
            "accounts",
            "representatives", "representative_create", "representative_delete",
            "direct_clients", "direct_clients_bind", "direct_clients_unbind",
            "exports", "export_create", "export_delete",
            "stat_data", "stat_data_drilldown", "stat_data_bytime", "stat_data_comparison",
            "logrequests", "logrequest", "logrequest_create", "logrequest_cancel",
            "logrequest_reset", "logrequest_clean", "logrequest_download",
            "messengers", "social_networks", "currencies", "timezones"
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Missing resource: {resource_name}"
    
    def test_client_get_counters_resource(self, metrika_config):
        """Test client can get counters resource."""
        client = ApiForgeClient(config=metrika_config)
        resource = client.get_resource("counters")
        
        assert resource.name == "counters"
        assert resource.path == "/management/v1/counters"
        assert resource.method == "GET"
    
    def test_client_get_stat_data_resource(self, metrika_config):
        """Test client can get stat_data resource."""
        client = ApiForgeClient(config=metrika_config)
        resource = client.get_resource("stat_data")
        
        assert resource.name == "stat_data"
        assert resource.path == "/stat/v1/data"
        assert resource.method == "GET"
    
    def test_client_context_manager(self, metrika_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=metrika_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) >= 40  # We have at least 40 resources


class TestYandexMetrikaConfigValidation:
    """Tests for Yandex Metrika configuration validation."""
    
    def test_config_file_exists(self, metrika_config_path):
        """Test config file exists."""
        assert metrika_config_path.exists()
        assert metrika_config_path.is_file()
    
    def test_config_is_valid_json(self, metrika_config_path):
        """Test config file is valid JSON."""
        with open(metrika_config_path) as f:
            config = json.load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self, metrika_config):
        """Test config has all required fields."""
        required_fields = ["base_url", "resources"]
        for field in required_fields:
            assert field in metrika_config, f"Missing required field: {field}"
    
    def test_config_resources_are_valid(self, metrika_config):
        """Test all resources have valid structure."""
        for name, resource in metrika_config["resources"].items():
            assert "path" in resource, f"Resource {name} missing path"
            assert "method" in resource, f"Resource {name} missing method"
            assert resource["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"], \
                f"Resource {name} has invalid method: {resource['method']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
