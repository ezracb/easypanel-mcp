"""
Basic tests for EasyPanel MCP Server.

Tests cover configuration, client, and tools functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from config import Config, EasyPanelConfig, ServerConfig
from src.client import EasyPanelClient
from src.tools.services import ServicesTools
from src.tools.deployments import DeploymentsTools
from src.tools.networks import NetworksTools
from src.tools.projects import ProjectsTools


class TestConfig:
    """Test configuration module."""
    
    def test_config_from_env(self):
        """Test creating config from environment variables."""
        with patch.dict('os.environ', {
            'EASYPANEL_URL': 'http://test.com',
            'EASYPANEL_API_KEY': 'test_key',
            'EASYPANEL_TIMEOUT': '60',
            'MCP_PORT': '9000'
        }):
            config = Config.from_env()
            
            assert config.easypanel.base_url == 'http://test.com'
            assert config.easypanel.api_key == 'test_key'
            assert config.easypanel.timeout == 60
            assert config.server.port == 9000
    
    def test_config_validate(self):
        """Test configuration validation."""
        config = Config(
            easypanel=EasyPanelConfig(api_key='test_key', base_url='http://test.com'),
            server=ServerConfig()
        )
        
        assert config.validate() is True
    
    def test_config_validate_missing_api_key(self):
        """Test validation fails without API key."""
        config = Config(
            easypanel=EasyPanelConfig(api_key='', base_url='http://test.com'),
            server=ServerConfig()
        )
        
        with pytest.raises(ValueError, match="EASYPANEL_API_KEY is required"):
            config.validate()


class TestEasyPanelClient:
    """Test EasyPanel API client."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        config = EasyPanelConfig(
            base_url='http://test.com',
            api_key='test_key',
            timeout=30
        )
        return EasyPanelClient(config)
    
    @pytest.mark.asyncio
    async def test_connect(self, client):
        """Test client connection."""
        await client.connect()
        
        assert client._client is not None
        await client.disconnect()
    
    @pytest.mark.asyncio
    async def test_disconnect(self, client):
        """Test client disconnection."""
        await client.connect()
        await client.disconnect()
        
        assert client._client is None
    
    @pytest.mark.asyncio
    async def test_request_without_connection(self, client):
        """Test request fails without connection."""
        with pytest.raises(RuntimeError, match="Client not connected"):
            await client._request("GET", "/api/services")


class TestServicesTools:
    """Test services tools."""
    
    @pytest.fixture
    def mock_client(self):
        """Create mock EasyPanel client."""
        client = AsyncMock()
        client.list_services = AsyncMock(return_value=[
            {"id": "svc_1", "name": "test-service"}
        ])
        client.get_service = AsyncMock(return_value={"id": "svc_1"})
        client.create_service = AsyncMock(return_value={"id": "svc_new"})
        client.delete_service = AsyncMock(return_value={"deleted": True})
        client.restart_service = AsyncMock(return_value={"status": "restarting"})
        client.get_service_logs = AsyncMock(return_value=["log line 1"])
        return client
    
    @pytest.fixture
    def services_tools(self, mock_client):
        """Create services tools instance."""
        return ServicesTools(mock_client)
    
    @pytest.mark.asyncio
    async def test_list_services(self, services_tools):
        """Test listing services."""
        result = await services_tools.execute("list_services", {})
        
        assert result["success"] is True
        assert len(result["data"]) == 1
    
    @pytest.mark.asyncio
    async def test_get_service(self, services_tools):
        """Test getting service details."""
        result = await services_tools.execute("get_service", {"service_id": "svc_1"})
        
        assert result["success"] is True
        assert result["data"]["id"] == "svc_1"
    
    @pytest.mark.asyncio
    async def test_create_service(self, services_tools):
        """Test creating service."""
        result = await services_tools.execute("create_service", {
            "name": "new-service",
            "project_id": "proj_1",
            "image": "nginx:latest"
        })
        
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self, services_tools):
        """Test unknown tool returns error."""
        result = await services_tools.execute("unknown_tool", {})
        
        assert result["success"] is False
        assert "error" in result


class TestDeploymentsTools:
    """Test deployments tools."""
    
    @pytest.fixture
    def mock_client(self):
        """Create mock EasyPanel client."""
        client = AsyncMock()
        client.list_deployments = AsyncMock(return_value=[])
        client.get_deployment = AsyncMock(return_value={"id": "deploy_1"})
        client.create_deployment = AsyncMock(return_value={"id": "deploy_new"})
        client.get_deployment_logs = AsyncMock(return_value=["log 1"])
        return client
    
    @pytest.fixture
    def deployments_tools(self, mock_client):
        """Create deployments tools instance."""
        return DeploymentsTools(mock_client)
    
    @pytest.mark.asyncio
    async def test_list_deployments(self, deployments_tools):
        """Test listing deployments."""
        result = await deployments_tools.execute("list_deployments", {})
        
        assert result["success"] is True


class TestNetworksTools:
    """Test networks tools."""
    
    @pytest.fixture
    def mock_client(self):
        """Create mock EasyPanel client."""
        client = AsyncMock()
        client.list_networks = AsyncMock(return_value=[])
        client.create_network = AsyncMock(return_value={"id": "net_1"})
        client.delete_network = AsyncMock(return_value={"deleted": True})
        return client
    
    @pytest.fixture
    def networks_tools(self, mock_client):
        """Create networks tools instance."""
        return NetworksTools(mock_client)
    
    @pytest.mark.asyncio
    async def test_create_internal_network(self, networks_tools):
        """Test creating internal network."""
        result = await networks_tools.execute("create_network", {
            "name": "internal-net",
            "internal": True
        })
        
        assert result["success"] is True
        assert "internal" in result["message"]


class TestProjectsTools:
    """Test projects tools."""
    
    @pytest.fixture
    def mock_client(self):
        """Create mock EasyPanel client."""
        client = AsyncMock()
        client.list_projects = AsyncMock(return_value=[])
        client.get_project = AsyncMock(return_value={"id": "proj_1"})
        client.create_project = AsyncMock(return_value={"id": "proj_new"})
        client.delete_project = AsyncMock(return_value={"deleted": True})
        return client
    
    @pytest.fixture
    def projects_tools(self, mock_client):
        """Create projects tools instance."""
        return ProjectsTools(mock_client)
    
    @pytest.mark.asyncio
    async def test_list_projects(self, projects_tools):
        """Test listing projects."""
        result = await projects_tools.execute("list_projects", {})
        
        assert result["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
