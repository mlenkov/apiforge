"""Tests for Yandex AdMetrica configuration."""

import json
import pytest
from pathlib import Path

from apiforge import ApiForgeClient
from apiforge.config import load_config


@pytest.fixture
def admetrica_config_path():
    """Path to Yandex AdMetrica config file."""
    return Path(__file__).parent.parent / "apiforge-configs" / "yandex" / "admetrica.json"


@pytest.fixture
def admetrica_config(admetrica_config_path):
    """Load Yandex AdMetrica configuration."""
    return load_config(admetrica_config_path)


class TestYandexAdMetricaConfig:
    """Tests for Yandex AdMetrica configuration file."""
    
    def test_config_loads(self, admetrica_config):
        """Test that config file loads successfully."""
        assert admetrica_config is not None
        assert "base_url" in admetrica_config
        assert "resources" in admetrica_config
    
    def test_base_url(self, admetrica_config):
        """Test base URL is correct."""
        assert admetrica_config["base_url"] == "https://api.media.metrika.yandex.net"
    
    def test_auth_structure(self, admetrica_config):
        """Test auth structure is correct."""
        assert "auth" in admetrica_config
        assert "token" in admetrica_config["auth"]
    
    def test_campaign_resources(self, admetrica_config):
        """Test campaign resources exist."""
        resources = admetrica_config["resources"]
        assert "campaigns" in resources
        assert "campaign" in resources
        assert "campaign_create" in resources
        assert "campaign_update" in resources
        assert "campaign_delete" in resources
        assert "campaign_copy" in resources
    
    def test_advertiser_resources(self, admetrica_config):
        """Test advertiser resources exist."""
        resources = admetrica_config["resources"]
        assert "advertisers" in resources
        assert "advertiser" in resources
        assert "advertiser_create" in resources
        assert "advertiser_update" in resources
        assert "advertiser_delete" in resources
    
    def test_goal_resources(self, admetrica_config):
        """Test goal resources exist."""
        resources = admetrica_config["resources"]
        assert "goals" in resources
        assert "goal" in resources
        assert "goal_create" in resources
        assert "goal_update" in resources
        assert "goal_delete" in resources
    
    def test_landing_page_resources(self, admetrica_config):
        """Test landing page resources exist."""
        resources = admetrica_config["resources"]
        assert "landing_pages" in resources
        assert "landing_page" in resources
        assert "landing_page_create" in resources
        assert "landing_page_update" in resources
        assert "landing_page_delete" in resources
    
    def test_grant_resources(self, admetrica_config):
        """Test grant resources exist."""
        resources = admetrica_config["resources"]
        assert "grants" in resources
        assert "grant_create" in resources
        assert "grant_delete" in resources
    
    def test_stat_resources(self, admetrica_config):
        """Test statistics resources exist."""
        resources = admetrica_config["resources"]
        assert "stat_data" in resources
        assert "stat_data_drilldown" in resources
        assert "stat_data_bytime" in resources
        assert "stat_summary" in resources
        assert "stat_comparison" in resources
    
    def test_campaign_parameters(self, admetrica_config):
        """Test campaign resource has parameters."""
        campaign = admetrica_config["resources"]["campaign"]
        assert "parameters" in campaign
        assert "campaign_id" in campaign["parameters"]
    
    def test_stat_data_parameters(self, admetrica_config):
        """Test stat_data resource has parameters."""
        stat_data = admetrica_config["resources"]["stat_data"]
        assert "parameters" in stat_data
        assert "ids" in stat_data["parameters"]
        assert "metrics" in stat_data["parameters"]
        assert "dimensions" in stat_data["parameters"]


class TestYandexAdMetricaClient:
    """Tests for Yandex AdMetrica client initialization."""
    
    def test_client_creation(self, admetrica_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=admetrica_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_all_resources(self, admetrica_config):
        """Test client loads all resources from config."""
        client = ApiForgeClient(config=admetrica_config)
        resources = client.list_resources()
        
        expected_resources = [
            "campaigns", "campaign", "campaign_create", "campaign_update",
            "campaign_delete", "campaign_copy",
            "advertisers", "advertiser", "advertiser_create", "advertiser_update", "advertiser_delete",
            "goals", "goal", "goal_create", "goal_update", "goal_delete",
            "landing_pages", "landing_page", "landing_page_create", "landing_page_update", "landing_page_delete",
            "grants", "grant_create", "grant_delete",
            "stat_data", "stat_data_drilldown", "stat_data_bytime", "stat_summary", "stat_comparison"
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Missing resource: {resource_name}"
    
    def test_client_get_campaigns_resource(self, admetrica_config):
        """Test client can get campaigns resource."""
        client = ApiForgeClient(config=admetrica_config)
        resource = client.get_resource("campaigns")
        
        assert resource.name == "campaigns"
        assert resource.path == "/v1/campaigns"
        assert resource.method == "GET"
    
    def test_client_get_stat_data_resource(self, admetrica_config):
        """Test client can get stat_data resource."""
        client = ApiForgeClient(config=admetrica_config)
        resource = client.get_resource("stat_data")
        
        assert resource.name == "stat_data"
        assert resource.path == "/v1/stat/data"
        assert resource.method == "GET"
    
    def test_client_context_manager(self, admetrica_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=admetrica_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) >= 25


class TestYandexAdMetricaConfigValidation:
    """Tests for Yandex AdMetrica configuration validation."""
    
    def test_config_file_exists(self, admetrica_config_path):
        """Test config file exists."""
        assert admetrica_config_path.exists()
        assert admetrica_config_path.is_file()
    
    def test_config_is_valid_json(self, admetrica_config_path):
        """Test config file is valid JSON."""
        with open(admetrica_config_path) as f:
            config = json.load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self, admetrica_config):
        """Test config has all required fields."""
        required_fields = ["base_url", "resources"]
        for field in required_fields:
            assert field in admetrica_config, f"Missing required field: {field}"
    
    def test_config_resources_are_valid(self, admetrica_config):
        """Test all resources have valid structure."""
        for name, resource in admetrica_config["resources"].items():
            assert "path" in resource, f"Resource {name} missing path"
            assert "method" in resource, f"Resource {name} missing method"
            assert resource["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"], \
                f"Resource {name} has invalid method: {resource['method']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
