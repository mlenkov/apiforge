"""Tests for Yandex Direct configuration."""

import json
import os
import pytest
from pathlib import Path

from apiforge import ApiForgeClient
from apiforge.config import load_config


@pytest.fixture
def direct_config_path():
    """Path to Yandex Direct config file."""
    return Path(__file__).parent.parent / "apiforge-configs" / "yandex" / "direct.json"


@pytest.fixture
def direct_config(direct_config_path):
    """Load Yandex Direct configuration."""
    return load_config(direct_config_path)


class TestYandexDirectConfig:
    """Tests for Yandex Direct configuration file."""
    
    def test_config_loads(self, direct_config):
        """Test that config file loads successfully."""
        assert direct_config is not None
        assert "base_url" in direct_config
        assert "resources" in direct_config
    
    def test_base_url(self, direct_config):
        """Test base URL is correct."""
        assert direct_config["base_url"] == "https://api.direct.yandex.com/json/v5"
    
    def test_sandbox_url(self, direct_config):
        """Test sandbox URL is present."""
        assert "sandbox_url" in direct_config
        assert direct_config["sandbox_url"] == "https://api-sandbox.direct.yandex.com/json/v5"
    
    def test_auth_structure(self, direct_config):
        """Test auth structure is correct."""
        assert "auth" in direct_config
        assert "token" in direct_config["auth"]
    
    def test_default_headers(self, direct_config):
        """Test default headers are present."""
        assert "default_headers" in direct_config
        headers = direct_config["default_headers"]
        assert "Accept-Language" in headers
        assert "Client-Login" in headers
        assert "processingMode" in headers
    
    def test_reports_resource(self, direct_config):
        """Test reports resource exists."""
        assert "reports" in direct_config["resources"]
        reports = direct_config["resources"]["reports"]
        assert reports["path"] == "/reports"
        assert reports["method"] == "POST"
    
    def test_reports_parameters(self, direct_config):
        """Test reports resource has required parameters."""
        reports = direct_config["resources"]["reports"]
        params = reports["parameters"]
        
        assert "SelectionCriteria" in params
        assert "FieldNames" in params
        assert "ReportName" in params
        assert "ReportType" in params
        assert "DateRangeType" in params
        assert "Format" in params
        assert "IncludeVAT" in params
    
    def test_report_types(self, direct_config):
        """Test report type enum values."""
        reports = direct_config["resources"]["reports"]
        report_type_param = reports["parameters"]["ReportType"]
        
        assert "enum" in report_type_param
        expected_types = [
            "ACCOUNT_PERFORMANCE_REPORT",
            "CAMPAIGN_PERFORMANCE_REPORT",
            "ADGROUP_PERFORMANCE_REPORT",
            "AD_PERFORMANCE_REPORT",
            "CRITERIA_PERFORMANCE_REPORT",
            "CUSTOM_REPORT",
            "REACH_AND_FREQUENCY_PERFORMANCE_REPORT",
            "SEARCH_QUERY_PERFORMANCE_REPORT"
        ]
        for report_type in expected_types:
            assert report_type in report_type_param["enum"]
    
    def test_date_range_types(self, direct_config):
        """Test date range type enum values."""
        reports = direct_config["resources"]["reports"]
        date_range = reports["parameters"]["DateRangeType"]
        
        assert "enum" in date_range
        expected_ranges = [
            "TODAY",
            "YESTERDAY",
            "LAST_7_DAYS",
            "LAST_30_DAYS",
            "CUSTOM_DATE",
            "ALL_TIME"
        ]
        for range_type in expected_ranges:
            assert range_type in date_range["enum"]
    
    def test_campaigns_resource(self, direct_config):
        """Test campaigns resource exists."""
        assert "campaigns" in direct_config["resources"]
        campaigns = direct_config["resources"]["campaigns"]
        assert campaigns["path"] == "/campaigns"
        assert campaigns["method"] == "GET"
    
    def test_adgroups_resource(self, direct_config):
        """Test adgroups resource exists."""
        assert "adgroups" in direct_config["resources"]
        adgroups = direct_config["resources"]["adgroups"]
        assert adgroups["path"] == "/adgroups"
        assert adgroups["method"] == "GET"
    
    def test_ads_resource(self, direct_config):
        """Test ads resource exists."""
        assert "ads" in direct_config["resources"]
        ads = direct_config["resources"]["ads"]
        assert ads["path"] == "/ads"
        assert ads["method"] == "GET"
    
    def test_keywords_resource(self, direct_config):
        """Test keywords resource exists."""
        assert "keywords" in direct_config["resources"]
        keywords = direct_config["resources"]["keywords"]
        assert keywords["path"] == "/keywords"
        assert keywords["method"] == "GET"


class TestYandexDirectClient:
    """Tests for Yandex Direct client initialization."""
    
    def test_client_creation(self, direct_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=direct_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_resources(self, direct_config):
        """Test client loads resources from config."""
        client = ApiForgeClient(config=direct_config)
        resources = client.list_resources()
        
        assert "reports" in resources
        assert "campaigns" in resources
        assert "adgroups" in resources
        assert "ads" in resources
        assert "keywords" in resources
    
    def test_client_get_reports_resource(self, direct_config):
        """Test client can get reports resource."""
        client = ApiForgeClient(config=direct_config)
        resource = client.get_resource("reports")
        
        assert resource.name == "reports"
        assert resource.path == "/reports"
        assert resource.method == "POST"
    
    def test_client_context_manager(self, direct_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=direct_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) > 0


class TestYandexDirectConfigValidation:
    """Tests for Yandex Direct configuration validation."""
    
    def test_config_file_exists(self, direct_config_path):
        """Test config file exists."""
        assert direct_config_path.exists()
        assert direct_config_path.is_file()
    
    def test_config_is_valid_json(self, direct_config_path):
        """Test config file is valid JSON."""
        with open(direct_config_path) as f:
            config = json.load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self, direct_config):
        """Test config has all required fields."""
        required_fields = ["base_url", "resources"]
        for field in required_fields:
            assert field in direct_config, f"Missing required field: {field}"
    
    def test_config_resources_are_valid(self, direct_config):
        """Test all resources have valid structure."""
        for name, resource in direct_config["resources"].items():
            assert "path" in resource, f"Resource {name} missing path"
            assert "method" in resource, f"Resource {name} missing method"
            assert resource["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"], \
                f"Resource {name} has invalid method: {resource['method']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
