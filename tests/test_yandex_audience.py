"""Tests for Yandex Audience configuration."""

import json
import pytest
from pathlib import Path

from apiforge import ApiForgeClient
from apiforge.config import load_config


@pytest.fixture
def audience_config_path():
    """Path to Yandex Audience config file."""
    return Path(__file__).parent.parent / "configs" / "yandex" / "audience.json"


@pytest.fixture
def audience_config(audience_config_path):
    """Load Yandex Audience configuration."""
    return load_config(audience_config_path)


class TestYandexAudienceConfig:
    """Tests for Yandex Audience configuration file."""
    
    def test_config_loads(self, audience_config):
        """Test that config file loads successfully."""
        assert audience_config is not None
        assert "base_url" in audience_config
        assert "resources" in audience_config
    
    def test_base_url(self, audience_config):
        """Test base URL is correct."""
        assert audience_config["base_url"] == "https://api-audience.yandex.ru/v2/management"
    
    def test_auth_structure(self, audience_config):
        """Test auth structure is correct."""
        assert "auth" in audience_config
        assert "token" in audience_config["auth"]
    
    def test_segment_resources(self, audience_config):
        """Test segment resources exist."""
        resources = audience_config["resources"]
        assert "segments" in resources
        assert "segment" in resources
        assert "segment_create" in resources
        assert "segment_update" in resources
        assert "segment_delete" in resources
        assert "segment_upload" in resources
        assert "segment_upload_check" in resources
        assert "segment_reach" in resources
        assert "segment_logs" in resources
        assert "segment_status" in resources
        assert "segment_progress" in resources
    
    def test_permission_resources(self, audience_config):
        """Test permission resources exist."""
        resources = audience_config["resources"]
        assert "permissions" in resources
        assert "permission_create" in resources
        assert "permission_delete" in resources
    
    def test_account_resources(self, audience_config):
        """Test account resources exist."""
        resources = audience_config["resources"]
        assert "accounts" in resources
        assert "representatives" in resources
        assert "representative_create" in resources
        assert "representative_update" in resources
        assert "representative_delete" in resources
    
    def test_pixel_resources(self, audience_config):
        """Test pixel resources exist."""
        resources = audience_config["resources"]
        assert "pixels" in resources
        assert "pixel" in resources
        assert "pixel_create" in resources
        assert "pixel_update" in resources
        assert "pixel_delete" in resources
        assert "pixel_update_counter_id" in resources
        assert "pixel_create_segment" in resources
        assert "pixel_segments" in resources
        assert "pixel_segment" in resources
        assert "pixel_segment_update" in resources
        assert "pixel_segment_delete" in resources
    
    def test_metrika_segment_resources(self, audience_config):
        """Test Metrika segment resources exist."""
        resources = audience_config["resources"]
        assert "metrika_segments" in resources
        assert "metrika_segment" in resources
    
    def test_geo_segment_resources(self, audience_config):
        """Test geo segment resources exist."""
        resources = audience_config["resources"]
        assert "geo_segments" in resources
        assert "geo_segment" in resources
        assert "geo_segment_create" in resources
        assert "geo_segment_update" in resources
        assert "geo_segment_delete" in resources
    
    def test_lookalike_segment_resources(self, audience_config):
        """Test lookalike segment resources exist."""
        resources = audience_config["resources"]
        assert "lookalike_segments" in resources
        assert "lookalike_segment" in resources
        assert "lookalike_segment_create" in resources
        assert "lookalike_segment_delete" in resources
    
    def test_combined_segment_resources(self, audience_config):
        """Test combined segment resources exist."""
        resources = audience_config["resources"]
        assert "combined_segments" in resources
        assert "combined_segment" in resources
        assert "combined_segment_create" in resources
        assert "combined_segment_update" in resources
        assert "combined_segment_delete" in resources
    
    def test_crm_segment_resources(self, audience_config):
        """Test CRM segment resources exist."""
        resources = audience_config["resources"]
        assert "crm_segments" in resources
        assert "crm_segment" in resources
        assert "crm_segment_create" in resources
        assert "crm_segment_update" in resources
        assert "crm_segment_delete" in resources
        assert "crm_segment_upload" in resources
        assert "crm_segment_upload_check" in resources
    
    def test_segment_parameters(self, audience_config):
        """Test segment resource has parameters."""
        segment = audience_config["resources"]["segment"]
        assert "parameters" in segment
        assert "segment_id" in segment["parameters"]


class TestYandexAudienceClient:
    """Tests for Yandex Audience client initialization."""
    
    def test_client_creation(self, audience_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=audience_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_all_resources(self, audience_config):
        """Test client loads all resources from config."""
        client = ApiForgeClient(config=audience_config)
        resources = client.list_resources()
        
        expected_resources = [
            "segments", "segment", "segment_create", "segment_update", "segment_delete",
            "segment_upload", "segment_upload_check", "segment_update_upload",
            "segment_reach", "segment_logs", "segment_status", "segment_progress",
            "permissions", "permission_create", "permission_delete",
            "accounts", "representatives", "representative_create", "representative_update", "representative_delete",
            "pixels", "pixel", "pixel_create", "pixel_update", "pixel_delete",
            "pixel_update_counter_id", "pixel_create_segment", "pixel_segments",
            "pixel_segment", "pixel_segment_update", "pixel_segment_delete",
            "metrika_segments", "metrika_segment",
            "geo_segments", "geo_segment", "geo_segment_create", "geo_segment_update", "geo_segment_delete",
            "lookalike_segments", "lookalike_segment", "lookalike_segment_create", "lookalike_segment_delete",
            "combined_segments", "combined_segment", "combined_segment_create", "combined_segment_update", "combined_segment_delete",
            "crm_segments", "crm_segment", "crm_segment_create", "crm_segment_update", "crm_segment_delete",
            "crm_segment_upload", "crm_segment_upload_check"
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Missing resource: {resource_name}"
    
    def test_client_get_segments_resource(self, audience_config):
        """Test client can get segments resource."""
        client = ApiForgeClient(config=audience_config)
        resource = client.get_resource("segments")
        
        assert resource.name == "segments"
        assert resource.path == "/segments"
        assert resource.method == "GET"
    
    def test_client_context_manager(self, audience_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=audience_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) >= 40


class TestYandexAudienceConfigValidation:
    """Tests for Yandex Audience configuration validation."""
    
    def test_config_file_exists(self, audience_config_path):
        """Test config file exists."""
        assert audience_config_path.exists()
        assert audience_config_path.is_file()
    
    def test_config_is_valid_json(self, audience_config_path):
        """Test config file is valid JSON."""
        with open(audience_config_path) as f:
            config = json.load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self, audience_config):
        """Test config has all required fields."""
        required_fields = ["base_url", "resources"]
        for field in required_fields:
            assert field in audience_config, f"Missing required field: {field}"
    
    def test_config_resources_are_valid(self, audience_config):
        """Test all resources have valid structure."""
        for name, resource in audience_config["resources"].items():
            assert "path" in resource, f"Resource {name} missing path"
            assert "method" in resource, f"Resource {name} missing method"
            assert resource["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"], \
                f"Resource {name} has invalid method: {resource['method']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
