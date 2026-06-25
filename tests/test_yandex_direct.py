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
    return Path(__file__).parent.parent / "configs" / "yandex" / "direct.json"


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
        assert campaigns["method"] == "POST"
        assert "methods" in campaigns
        assert "add" in campaigns["methods"]
        assert "get" in campaigns["methods"]
        assert "update" in campaigns["methods"]
        assert "delete" in campaigns["methods"]
    
    def test_adgroups_resource(self, direct_config):
        """Test adgroups resource exists."""
        assert "adgroups" in direct_config["resources"]
        adgroups = direct_config["resources"]["adgroups"]
        assert adgroups["path"] == "/adgroups"
        assert adgroups["method"] == "POST"
        assert "methods" in adgroups
        assert "add" in adgroups["methods"]
        assert "get" in adgroups["methods"]
    
    def test_ads_resource(self, direct_config):
        """Test ads resource exists."""
        assert "ads" in direct_config["resources"]
        ads = direct_config["resources"]["ads"]
        assert ads["path"] == "/ads"
        assert ads["method"] == "POST"
        assert "methods" in ads
        assert "add" in ads["methods"]
        assert "get" in ads["methods"]
        assert "moderate" in ads["methods"]
    
    def test_keywords_resource(self, direct_config):
        """Test keywords resource exists."""
        assert "keywords" in direct_config["resources"]
        keywords = direct_config["resources"]["keywords"]
        assert keywords["path"] == "/keywords"
        assert keywords["method"] == "POST"
        assert "methods" in keywords
        assert "add" in keywords["methods"]
        assert "get" in keywords["methods"]
    
    def test_bids_resource(self, direct_config):
        """Test bids resource exists."""
        assert "bids" in direct_config["resources"]
        bids = direct_config["resources"]["bids"]
        assert bids["path"] == "/bids"
        assert bids["method"] == "POST"
        assert "methods" in bids
        assert "get" in bids["methods"]
        assert "set" in bids["methods"]
        assert "setAuto" in bids["methods"]
    
    def test_keywordbids_resource(self, direct_config):
        """Test keywordbids resource exists."""
        assert "keywordbids" in direct_config["resources"]
        keywordbids = direct_config["resources"]["keywordbids"]
        assert keywordbids["path"] == "/keywordbids"
        assert keywordbids["method"] == "POST"
    
    def test_bidmodifiers_resource(self, direct_config):
        """Test bidmodifiers resource exists."""
        assert "bidmodifiers" in direct_config["resources"]
        bidmodifiers = direct_config["resources"]["bidmodifiers"]
        assert bidmodifiers["path"] == "/bidmodifiers"
        assert bidmodifiers["method"] == "POST"
        assert "methods" in bidmodifiers
        assert "add" in bidmodifiers["methods"]
        assert "delete" in bidmodifiers["methods"]
    
    def test_negativekeywordsharedsets_resource(self, direct_config):
        """Test negativekeywordsharedsets resource exists."""
        assert "negativekeywordsharedsets" in direct_config["resources"]
        nks = direct_config["resources"]["negativekeywordsharedsets"]
        assert nks["path"] == "/negativekeywordsharedsets"
        assert nks["method"] == "POST"
    
    def test_keywordsresearch_resource(self, direct_config):
        """Test keywordsresearch resource exists."""
        assert "keywordsresearch" in direct_config["resources"]
        kr = direct_config["resources"]["keywordsresearch"]
        assert kr["path"] == "/keywordsresearch"
        assert kr["method"] == "POST"
        assert "methods" in kr
        assert "deduplicate" in kr["methods"]
        assert "hasSearchVolume" in kr["methods"]
    
    def test_businesses_resource(self, direct_config):
        """Test businesses resource exists."""
        assert "businesses" in direct_config["resources"]
        businesses = direct_config["resources"]["businesses"]
        assert businesses["path"] == "/businesses"
        assert businesses["method"] == "POST"
    
    def test_adimages_resource(self, direct_config):
        """Test adimages resource exists."""
        assert "adimages" in direct_config["resources"]
        adimages = direct_config["resources"]["adimages"]
        assert adimages["path"] == "/adimages"
        assert adimages["method"] == "POST"
        assert "methods" in adimages
        assert "add" in adimages["methods"]
        assert "delete" in adimages["methods"]
    
    def test_creatives_resource(self, direct_config):
        """Test creatives resource exists."""
        assert "creatives" in direct_config["resources"]
        creatives = direct_config["resources"]["creatives"]
        assert creatives["path"] == "/creatives"
        assert creatives["method"] == "POST"
    
    def test_advideos_resource(self, direct_config):
        """Test advideos resource exists."""
        assert "advideos" in direct_config["resources"]
        advideos = direct_config["resources"]["advideos"]
        assert advideos["path"] == "/advideos"
        assert advideos["method"] == "POST"
    
    def test_turbopages_resource(self, direct_config):
        """Test turbopages resource exists."""
        assert "turbopages" in direct_config["resources"]
        turbopages = direct_config["resources"]["turbopages"]
        assert turbopages["path"] == "/turbopages"
        assert turbopages["method"] == "POST"
    
    def test_leads_resource(self, direct_config):
        """Test leads resource exists."""
        assert "leads" in direct_config["resources"]
        leads = direct_config["resources"]["leads"]
        assert leads["path"] == "/leads"
        assert leads["method"] == "POST"
    
    def test_sitelinks_resource(self, direct_config):
        """Test sitelinks resource exists."""
        assert "sitelinks" in direct_config["resources"]
        sitelinks = direct_config["resources"]["sitelinks"]
        assert sitelinks["path"] == "/sitelinks"
        assert sitelinks["method"] == "POST"
        assert "methods" in sitelinks
        assert "add" in sitelinks["methods"]
        assert "delete" in sitelinks["methods"]
    
    def test_adextensions_resource(self, direct_config):
        """Test adextensions resource exists."""
        assert "adextensions" in direct_config["resources"]
        adextensions = direct_config["resources"]["adextensions"]
        assert adextensions["path"] == "/adextensions"
        assert adextensions["method"] == "POST"
    
    def test_audiencetargets_resource(self, direct_config):
        """Test audiencetargets resource exists."""
        assert "audiencetargets" in direct_config["resources"]
        at = direct_config["resources"]["audiencetargets"]
        assert at["path"] == "/audiencetargets"
        assert at["method"] == "POST"
        assert "methods" in at
        assert "add" in at["methods"]
        assert "setBids" in at["methods"]
    
    def test_retargetinglists_resource(self, direct_config):
        """Test retargetinglists resource exists."""
        assert "retargetinglists" in direct_config["resources"]
        rl = direct_config["resources"]["retargetinglists"]
        assert rl["path"] == "/retargetinglists"
        assert rl["method"] == "POST"
    
    def test_clients_resource(self, direct_config):
        """Test clients resource exists."""
        assert "clients" in direct_config["resources"]
        clients = direct_config["resources"]["clients"]
        assert clients["path"] == "/clients"
        assert clients["method"] == "POST"
        assert "methods" in clients
        assert "get" in clients["methods"]
        assert "update" in clients["methods"]
    
    def test_agencyclients_resource(self, direct_config):
        """Test agencyclients resource exists."""
        assert "agencyclients" in direct_config["resources"]
        ac = direct_config["resources"]["agencyclients"]
        assert ac["path"] == "/agencyclients"
        assert ac["method"] == "POST"
    
    def test_feeds_resource(self, direct_config):
        """Test feeds resource exists."""
        assert "feeds" in direct_config["resources"]
        feeds = direct_config["resources"]["feeds"]
        assert feeds["path"] == "/feeds"
        assert feeds["method"] == "POST"
        assert "methods" in feeds
        assert "add" in feeds["methods"]
        assert "delete" in feeds["methods"]
    
    def test_dictionaries_resource(self, direct_config):
        """Test dictionaries resource exists."""
        assert "dictionaries" in direct_config["resources"]
        dicts = direct_config["resources"]["dictionaries"]
        assert dicts["path"] == "/dictionaries"
        assert dicts["method"] == "POST"
    
    def test_changes_resource(self, direct_config):
        """Test changes resource exists."""
        assert "changes" in direct_config["resources"]
        changes = direct_config["resources"]["changes"]
        assert changes["path"] == "/changes"
        assert changes["method"] == "POST"
        assert "methods" in changes
        assert "check" in changes["methods"]
        assert "checkCampaigns" in changes["methods"]
    
    def test_strategies_resource(self, direct_config):
        """Test strategies resource exists."""
        assert "strategies" in direct_config["resources"]
        strategies = direct_config["resources"]["strategies"]
        assert strategies["path"] == "/strategies"
        assert strategies["method"] == "POST"
    
    def test_accountlogins_resource(self, direct_config):
        """Test accountlogins resource exists."""
        assert "accountlogins" in direct_config["resources"]
        al = direct_config["resources"]["accountlogins"]
        assert al["path"] == "/accountlogins"
        assert al["method"] == "POST"
    
    def test_balance_resource(self, direct_config):
        """Test balance resource exists."""
        assert "balance" in direct_config["resources"]
        balance = direct_config["resources"]["balance"]
        assert balance["path"] == "/balance"
        assert balance["method"] == "POST"
    
    def test_units_resource(self, direct_config):
        """Test units resource exists."""
        assert "units" in direct_config["resources"]
        units = direct_config["resources"]["units"]
        assert units["path"] == "/units"
        assert units["method"] == "POST"
    
    def test_grants_resource(self, direct_config):
        """Test grants resource exists."""
        assert "grants" in direct_config["resources"]
        grants = direct_config["resources"]["grants"]
        assert grants["path"] == "/grants"
        assert grants["method"] == "POST"
    
    def test_all_resources_have_methods_or_method(self, direct_config):
        """Test all resources have methods defined or a single method."""
        for name, resource in direct_config["resources"].items():
            has_methods = "methods" in resource and len(resource["methods"]) > 0
            has_method = "method" in resource
            assert has_methods or has_method, f"Resource {name} missing methods/method"


class TestYandexDirectClient:
    """Tests for Yandex Direct client initialization."""
    
    def test_client_creation(self, direct_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=direct_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_all_resources(self, direct_config):
        """Test client loads all resources from config."""
        client = ApiForgeClient(config=direct_config)
        resources = client.list_resources()
        
        expected_resources = [
            "reports", "campaigns", "adgroups", "ads", "keywords",
            "bids", "keywordbids", "bidmodifiers", "negativekeywordsharedsets",
            "keywordsresearch", "businesses", "adimages", "creatives",
            "advideos", "turbopages", "leads", "sitelinks", "adextensions",
            "audiencetargets", "retargetinglists", "clients", "agencyclients",
            "feeds", "dictionaries", "changes", "strategies", "accountlogins",
            "balance", "units", "grants"
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Missing resource: {resource_name}"
    
    def test_client_get_reports_resource(self, direct_config):
        """Test client can get reports resource."""
        client = ApiForgeClient(config=direct_config)
        resource = client.get_resource("reports")
        
        assert resource.name == "reports"
        assert resource.path == "/reports"
        assert resource.method == "POST"
    
    def test_client_get_campaigns_resource(self, direct_config):
        """Test client can get campaigns resource."""
        client = ApiForgeClient(config=direct_config)
        resource = client.get_resource("campaigns")
        
        assert resource.name == "campaigns"
        assert resource.path == "/campaigns"
        assert resource.method == "POST"
    
    def test_client_get_ads_resource(self, direct_config):
        """Test client can get ads resource."""
        client = ApiForgeClient(config=direct_config)
        resource = client.get_resource("ads")
        
        assert resource.name == "ads"
        assert resource.path == "/ads"
        assert resource.method == "POST"
    
    def test_client_get_keywords_resource(self, direct_config):
        """Test client can get keywords resource."""
        client = ApiForgeClient(config=direct_config)
        resource = client.get_resource("keywords")
        
        assert resource.name == "keywords"
        assert resource.path == "/keywords"
        assert resource.method == "POST"
    
    def test_client_context_manager(self, direct_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=direct_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) >= 30  # We have at least 30 resources


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
