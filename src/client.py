"""
EasyPanel API Client.

Handles all communication with the EasyPanel API.
"""

import httpx
import logging
from typing import Any, Optional
from config import EasyPanelConfig

logger = logging.getLogger(__name__)


class EasyPanelClient:
    """Client for interacting with EasyPanel API."""
    
    def __init__(self, config: EasyPanelConfig):
        """
        Initialize EasyPanel client.
        
        Args:
            config: EasyPanel configuration settings
        """
        self.base_url = config.base_url.rstrip("/")
        self.api_key = config.api_key
        self.timeout = config.timeout
        self.verify_ssl = config.verify_ssl
        
        self._client: Optional[httpx.AsyncClient] = None
    
    async def connect(self) -> None:
        """Establish connection to EasyPanel API."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        logger.info(f"Connected to EasyPanel at {self.base_url}")
    
    async def disconnect(self) -> None:
        """Close connection to EasyPanel API."""
        if self._client:
            await self._client.aclose()
            logger.info("Disconnected from EasyPanel")
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Make HTTP request to EasyPanel API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            response = await self._client.request(
                method=method,
                url=endpoint,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise
    
    # Service Management
    async def list_services(self, project_id: Optional[str] = None) -> list[dict[str, Any]]:
        """
        List all services.
        
        Args:
            project_id: Optional project ID to filter services
            
        Returns:
            List of services
        """
        params = {"projectId": project_id} if project_id else {}
        response = await self._request("GET", "/api/services", params=params)
        return response.get("data", [])
    
    async def get_service(self, service_id: str) -> dict[str, Any]:
        """
        Get service details.
        
        Args:
            service_id: Service ID
            
        Returns:
            Service details
        """
        return await self._request("GET", f"/api/services/{service_id}")
    
    async def create_service(
        self,
        name: str,
        project_id: str,
        image: str,
        config: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Create a new service.
        
        Args:
            name: Service name
            project_id: Project ID
            image: Docker image
            config: Additional configuration
            
        Returns:
            Created service details
        """
        data = {
            "name": name,
            "projectId": project_id,
            "image": image,
            **(config or {})
        }
        return await self._request("POST", "/api/services", data=data)
    
    async def update_service(
        self,
        service_id: str,
        config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update service configuration.
        
        Args:
            service_id: Service ID
            config: New configuration
            
        Returns:
            Updated service details
        """
        return await self._request("PUT", f"/api/services/{service_id}", data=config)
    
    async def delete_service(self, service_id: str) -> dict[str, Any]:
        """
        Delete a service.
        
        Args:
            service_id: Service ID
            
        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/api/services/{service_id}")
    
    async def restart_service(self, service_id: str) -> dict[str, Any]:
        """
        Restart a service.
        
        Args:
            service_id: Service ID
            
        Returns:
            Restart confirmation
        """
        return await self._request("POST", f"/api/services/{service_id}/restart")
    
    async def get_service_logs(
        self,
        service_id: str,
        lines: int = 100
    ) -> list[str]:
        """
        Get service logs.
        
        Args:
            service_id: Service ID
            lines: Number of log lines to retrieve
            
        Returns:
            List of log lines
        """
        params = {"lines": lines}
        response = await self._request("GET", f"/api/services/{service_id}/logs", params=params)
        return response.get("data", [])
    
    # Project Management
    async def list_projects(self) -> list[dict[str, Any]]:
        """
        List all projects.
        
        Returns:
            List of projects
        """
        response = await self._request("GET", "/api/projects")
        return response.get("data", [])
    
    async def get_project(self, project_id: str) -> dict[str, Any]:
        """
        Get project details.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project details
        """
        return await self._request("GET", f"/api/projects/{project_id}")
    
    async def create_project(
        self,
        name: str,
        description: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            Created project details
        """
        data = {"name": name}
        if description:
            data["description"] = description
        return await self._request("POST", "/api/projects", data=data)
    
    async def delete_project(self, project_id: str) -> dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/api/projects/{project_id}")
    
    # Network Management
    async def list_networks(self) -> list[dict[str, Any]]:
        """
        List all networks.
        
        Returns:
            List of networks
        """
        response = await self._request("GET", "/api/networks")
        return response.get("data", [])
    
    async def create_network(
        self,
        name: str,
        internal: bool = False,
        driver: str = "overlay"
    ) -> dict[str, Any]:
        """
        Create a new network.
        
        Args:
            name: Network name
            internal: Whether network is internal (isolated)
            driver: Network driver
            
        Returns:
            Created network details
        """
        data = {
            "name": name,
            "internal": internal,
            "driver": driver
        }
        return await self._request("POST", "/api/networks", data=data)
    
    async def delete_network(self, network_id: str) -> dict[str, Any]:
        """
        Delete a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/api/networks/{network_id}")
    
    # Deployment Management
    async def list_deployments(self, project_id: Optional[str] = None) -> list[dict[str, Any]]:
        """
        List all deployments.
        
        Args:
            project_id: Optional project ID to filter deployments
            
        Returns:
            List of deployments
        """
        params = {"projectId": project_id} if project_id else {}
        response = await self._request("GET", "/api/deployments", params=params)
        return response.get("data", [])
    
    async def get_deployment(self, deployment_id: str) -> dict[str, Any]:
        """
        Get deployment details.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Deployment details
        """
        return await self._request("GET", f"/api/deployments/{deployment_id}")
    
    async def create_deployment(
        self,
        project_id: str,
        service_id: str,
        image: str,
        config: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Create a new deployment.
        
        Args:
            project_id: Project ID
            service_id: Service ID
            image: Docker image
            config: Additional configuration
            
        Returns:
            Created deployment details
        """
        data = {
            "projectId": project_id,
            "serviceId": service_id,
            "image": image,
            **(config or {})
        }
        return await self._request("POST", "/api/deployments", data=data)
    
    async def get_deployment_logs(self, deployment_id: str) -> list[str]:
        """
        Get deployment logs.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            List of log lines
        """
        response = await self._request("GET", f"/api/deployments/{deployment_id}/logs")
        return response.get("data", [])
    
    # System Information
    async def get_system_info(self) -> dict[str, Any]:
        """
        Get system information.
        
        Returns:
            System information
        """
        return await self._request("GET", "/api/system/info")
    
    async def health_check(self) -> bool:
        """
        Check EasyPanel API health.
        
        Returns:
            True if API is healthy
        """
        try:
            response = await self._request("GET", "/api/health")
            return response.get("status") == "healthy"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
