"""Tests for Yandex Webmaster configuration."""

import json
import pytest
from pathlib import Path

from apiforge import ApiForgeClient
from apiforge.config import load_config


@pytest.fixture
def webmaster_config_path():
    """Path to Yandex Webmaster config file."""
    return Path(__file__).parent.parent / "apiforge-configs" / "yandex" / "webmaster.json"


@pytest.fixture
def webmaster_config(webmaster_config_path):
    """Load Yandex Webmaster configuration."""
    return load_config(webmaster_config_path)


class TestYandexWebmasterConfig:
    """Tests for Yandex Webmaster configuration file."""
    
    def test_config_loads(self, webmaster_config):
        """Test that config file loads successfully."""
        assert webmaster_config is not None
        assert "base_url" in webmaster_config
        assert "resources" in webmaster_config
    
    def test_base_url(self, webmaster_config):
        """Test base URL is correct."""
        assert webmaster_config["base_url"] == "https://api.webmaster.yandex.net"
    
    def test_auth_structure(self, webmaster_config):
        """Test auth structure is correct."""
        assert "auth" in webmaster_config
        assert "token" in webmaster_config["auth"]
    
    def test_user_resource(self, webmaster_config):
        """Test user resource exists."""
        assert "user" in webmaster_config["resources"]
        user = webmaster_config["resources"]["user"]
        assert user["path"] == "/user/"
        assert user["method"] == "GET"
    
    def test_hosts_resource(self, webmaster_config):
        """Test hosts resource exists."""
        assert "hosts" in webmaster_config["resources"]
        hosts = webmaster_config["resources"]["hosts"]
        assert "user_id" in hosts["parameters"]
    
    def test_host_resource(self, webmaster_config):
        """Test host resource exists."""
        assert "host" in webmaster_config["resources"]
        host = webmaster_config["resources"]["host"]
        assert "user_id" in host["parameters"]
        assert "host_id" in host["parameters"]
    
    def test_verification_resources(self, webmaster_config):
        """Test verification resources exist."""
        resources = webmaster_config["resources"]
        assert "host_verification" in resources
        assert "host_verification_start" in resources
    
    def test_sitemaps_resources(self, webmaster_config):
        """Test sitemaps resources exist."""
        resources = webmaster_config["resources"]
        assert "host_sitemaps" in resources
        assert "host_user_added_sitemaps" in resources
        assert "host_user_added_sitemap_add" in resources
        assert "host_user_added_sitemap_delete" in resources
    
    def test_search_queries_resources(self, webmaster_config):
        """Test search queries resources exist."""
        resources = webmaster_config["resources"]
        assert "host_search_queries_popular" in resources
        assert "host_search_queries_history_all" in resources
        assert "host_search_queries_history" in resources
        assert "host_query_analytics" in resources
    
    def test_recrawl_resources(self, webmaster_config):
        """Test recrawl resources exist."""
        resources = webmaster_config["resources"]
        assert "host_recrawl_queue" in resources
        assert "host_recrawl_add" in resources
        assert "host_recrawl_quota" in resources
        assert "host_recrawl_task" in resources
    
    def test_diagnostics_resources(self, webmaster_config):
        """Test diagnostics resources exist."""
        resources = webmaster_config["resources"]
        assert "host_diagnostics" in resources
    
    def test_indexing_resources(self, webmaster_config):
        """Test indexing resources exist."""
        resources = webmaster_config["resources"]
        assert "host_indexing_history" in resources
        assert "host_indexing_samples" in resources
        assert "host_insearch_history" in resources
        assert "host_insearch_samples" in resources
    
    def test_links_resources(self, webmaster_config):
        """Test links resources exist."""
        resources = webmaster_config["resources"]
        assert "host_links_internal_samples" in resources
        assert "host_links_internal_history" in resources
        assert "host_links_external_samples" in resources
        assert "host_links_external_history" in resources
    
    def test_feeds_resources(self, webmaster_config):
        """Test feeds resources exist."""
        resources = webmaster_config["resources"]
        assert "host_feeds_list" in resources
        assert "host_feed_add_start" in resources
        assert "host_feed_add_info" in resources
        assert "host_feeds_batch_add" in resources
        assert "host_feeds_batch_remove" in resources


class TestYandexWebmasterClient:
    """Tests for Yandex Webmaster client initialization."""
    
    def test_client_creation(self, webmaster_config):
        """Test client can be created with config."""
        client = ApiForgeClient(config=webmaster_config)
        assert client is not None
        assert hasattr(client, "_adapter")
    
    def test_client_has_all_resources(self, webmaster_config):
        """Test client loads all resources from config."""
        client = ApiForgeClient(config=webmaster_config)
        resources = client.list_resources()
        
        expected_resources = [
            "user", "hosts", "host_add", "host", "host_delete",
            "host_summary", "host_important_urls", "host_important_urls_history",
            "host_verification", "host_verification_start", "host_owners",
            "host_sitemaps", "host_sitemap",
            "host_user_added_sitemaps", "host_user_added_sitemap_add",
            "host_user_added_sitemap_info", "host_user_added_sitemap_delete",
            "host_sqi_history",
            "host_search_queries_popular", "host_search_queries_history_all",
            "host_search_queries_history", "host_query_analytics",
            "host_recrawl_queue", "host_recrawl_add", "host_recrawl_quota", "host_recrawl_task",
            "host_diagnostics",
            "host_indexing_history", "host_indexing_samples",
            "host_insearch_history", "host_insearch_samples",
            "host_search_events_history", "host_search_events_samples",
            "host_links_internal_samples", "host_links_internal_history",
            "host_links_external_samples", "host_links_external_history",
            "host_feeds_list", "host_feed_add_start", "host_feed_add_info",
            "host_feeds_batch_add", "host_feeds_batch_remove"
        ]
        
        for resource_name in expected_resources:
            assert resource_name in resources, f"Missing resource: {resource_name}"
    
    def test_client_get_user_resource(self, webmaster_config):
        """Test client can get user resource."""
        client = ApiForgeClient(config=webmaster_config)
        resource = client.get_resource("user")
        
        assert resource.name == "user"
        assert resource.path == "/user/"
        assert resource.method == "GET"
    
    def test_client_context_manager(self, webmaster_config):
        """Test client works as context manager."""
        with ApiForgeClient(config=webmaster_config) as client:
            assert client is not None
            resources = client.list_resources()
            assert len(resources) >= 30


class TestYandexWebmasterConfigValidation:
    """Tests for Yandex Webmaster configuration validation."""
    
    def test_config_file_exists(self, webmaster_config_path):
        """Test config file exists."""
        assert webmaster_config_path.exists()
        assert webmaster_config_path.is_file()
    
    def test_config_is_valid_json(self, webmaster_config_path):
        """Test config file is valid JSON."""
        with open(webmaster_config_path) as f:
            config = json.load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self, webmaster_config):
        """Test config has all required fields."""
        required_fields = ["base_url", "resources"]
        for field in required_fields:
            assert field in webmaster_config, f"Missing required field: {field}"
    
    def test_config_resources_are_valid(self, webmaster_config):
        """Test all resources have valid structure."""
        for name, resource in webmaster_config["resources"].items():
            assert "path" in resource, f"Resource {name} missing path"
            assert "method" in resource, f"Resource {name} missing method"
            assert resource["method"] in ["GET", "POST", "PUT", "DELETE", "PATCH"], \
                f"Resource {name} has invalid method: {resource['method']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
