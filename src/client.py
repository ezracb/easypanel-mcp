"""
Enhanced EasyPanel Client with advanced features.

Adds support for logs, networks discovery, and auto-scaling
by combining tRPC API calls with smart inference.
"""

import httpx
import logging
import json
from typing import Any, Optional
from config import EasyPanelConfig

logger = logging.getLogger(__name__)


class EasyPanelClient:
    """Enhanced client for interacting with EasyPanel API using tRPC."""

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
        self._token: Optional[str] = None

    async def connect(self) -> None:
        """Establish connection to EasyPanel API."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        # If API key looks like email:password, authenticate via tRPC
        if ":" in self.api_key and "@" in self.api_key:
            await self._authenticate_with_email_password()
        else:
            # Use API key as Bearer token (session token)
            self._client.headers["Authorization"] = f"Bearer {self.api_key}"
            logger.info(f"Connected to EasyPanel at {self.base_url} (Bearer token auth)")

    async def _authenticate_with_email_password(self) -> None:
        """Authenticate using email and password via tRPC."""
        try:
            email, password = self.api_key.split(":", 1)
            response = await self._client.post(
                "/api/trpc/auth.login",
                json={"json": {"email": email, "password": password}}
            )
            response.raise_for_status()
            result = response.json()
            token = result.get("result", {}).get("data", {}).get("json", {}).get("token")
            
            if token:
                self._token = token
                self._client.headers["Authorization"] = token
                logger.info(f"Authenticated to EasyPanel as {email}")
            else:
                raise RuntimeError("No token received from auth.login")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Close connection to EasyPanel API."""
        if self._client:
            await self._client.aclose()
            logger.info("Disconnected from EasyPanel")

    async def _trpc_request(
        self,
        procedure: str,
        input_data: Optional[dict[str, Any]] = None,
        method: str = "POST"
    ) -> Any:
        """
        Make tRPC request to EasyPanel API.

        Args:
            procedure: tRPC procedure name
            input_data: Input data for the procedure
            method: HTTP method (GET or POST)

        Returns:
            Extracted data from tRPC response
        """
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        endpoint = f"/api/trpc/{procedure}"
        
        try:
            query_procedures = ["list", "get", "inspect", "stats", "info", "check", "public"]
            is_query = any(q in procedure.lower() for q in query_procedures)
            
            if is_query or method == "GET":
                if input_data:
                    input_json = json.dumps({"json": input_data})
                    response = await self._client.get(endpoint, params={"input": input_json})
                else:
                    response = await self._client.get(endpoint)
            else:
                payload = {"json": input_data} if input_data else {"json": None}
                response = await self._client.post(endpoint, json=payload)
            
            response.raise_for_status()
            result = response.json()
            
            # Extract data using common tRPC patterns
            res_obj = result.get("result", {})
            data_obj = res_obj.get("data", {})
            
            if isinstance(data_obj, dict) and "json" in data_obj:
                return data_obj["json"]
            
            return data_obj
            
        except httpx.HTTPStatusError as e:
            error_msg = e.response.text
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", {}).get("json", {}).get("message", error_msg)
            except:
                pass
            logger.error(f"tRPC error [{procedure}]: {error_msg}")
            raise RuntimeError(f"tRPC error: {error_msg}")
        except Exception as e:
            logger.error(f"Request error [{procedure}]: {str(e)}")
            raise

    # ========== Project Management ==========
    
    async def list_projects(self) -> list[dict[str, Any]]:
        """List all projects."""
        try:
            # listProjectsAndServices is likely a query
            result = await self._trpc_request("projects.listProjectsAndServices", method="GET")
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and "data" in result:
                return result["data"]
            return []
        except Exception as e:
            logger.error(f"Error listing projects: {e}")
            return []

    async def get_project(self, project_id: str) -> dict[str, Any]:
        """Get project details (inspect)."""
        try:
            return await self._trpc_request("projects.inspectProject", {"id": project_id}, method="GET")
        except Exception as e:
            logger.error(f"Error getting project: {e}")
            return {}

    async def create_project(
        self,
        name: str,
        description: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new project."""
        try:
            data = {"name": name}
            if description:
                data["description"] = description
            return await self._trpc_request("projects.createProject", data)
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return {}

    async def delete_project(self, project_id: str) -> dict[str, Any]:
        """Delete a project."""
        try:
            return await self._trpc_request("projects.destroyProject", {"id": project_id})
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            return {}

    # ========== Service Management ==========
    
    async def list_services(self, project_id: Optional[str] = None) -> list[dict[str, Any]]:
        """List all services, optionally filtered by project."""
        try:
            projects = await self.list_projects()
            
            if project_id:
                for proj in projects:
                    if proj.get("id") == project_id or proj.get("name") == project_id:
                        return proj.get("services", [])
                return []
            else:
                services = []
                for proj in projects:
                    proj_services = proj.get("services", [])
                    for s in proj_services:
                        s["projectName"] = proj.get("name")
                        s["projectId"] = proj.get("id")
                    services.extend(proj_services)
                return services
        except Exception as e:
            logger.error(f"Error listing services: {e}")
            return []

    async def get_service(self, service_id: str) -> dict[str, Any]:
        """Get service details (inspect)."""
        try:
            return await self._trpc_request("services.app.inspectService", {"id": service_id}, method="GET")
        except Exception as e:
            logger.error(f"Error getting service: {e}")
            return {}

    async def create_service(
        self,
        name: str,
        project_id: str,
        image: str,
        config: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Create a new service (app type)."""
        try:
            # We need the real project UUID. If project_id looks like a name, try to find it.
            real_project_id = project_id
            if "-" not in project_id:
                projects = await self.list_projects()
                for p in projects:
                    if p.get("name") == project_id:
                        real_project_id = p.get("id")
                        break
            
            data = {
                "projectId": real_project_id,
                "name": name,
                "sourceImage": image,
                **(config or {})
            }
            return await self._trpc_request("services.app.createService", data)
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            return {}

    async def deploy_service(self, service_id: str) -> dict[str, Any]:
        """Deploy/redeploy a service."""
        try:
            return await self._trpc_request("services.app.deployService", {"id": service_id})
        except Exception as e:
            logger.error(f"Error deploying service: {e}")
            return {}

    async def restart_service(self, service_id: str) -> dict[str, Any]:
        """Restart a service."""
        try:
            return await self._trpc_request("services.app.restartService", {"id": service_id})
        except Exception as e:
            logger.error(f"Error restarting service: {e}")
            return {}
