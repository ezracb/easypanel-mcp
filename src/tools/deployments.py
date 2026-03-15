"""
Deployments Tool Module.

Provides tools for managing EasyPanel deployments.
"""

import logging
from typing import Any
from src.client import EasyPanelClient

logger = logging.getLogger(__name__)


class DeploymentsTools:
    """Tools for managing deployments in EasyPanel."""
    
    def __init__(self, client: EasyPanelClient):
        """
        Initialize deployments tools.
        
        Args:
            client: EasyPanel API client
        """
        self.client = client
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """
        Get MCP tool definitions for deployments.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "list_deployments",
                "description": "List all deployments in EasyPanel, optionally filtered by project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Optional project ID to filter deployments"
                        }
                    }
                }
            },
            {
                "name": "get_deployment",
                "description": "Get detailed information about a specific deployment",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "deployment_id": {
                            "type": "string",
                            "description": "Deployment ID"
                        }
                    },
                    "required": ["deployment_id"]
                }
            },
            {
                "name": "create_deployment",
                "description": "Create a new deployment in EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        },
                        "image": {
                            "type": "string",
                            "description": "Docker image to deploy"
                        },
                        "config": {
                            "type": "object",
                            "description": "Additional deployment configuration"
                        }
                    },
                    "required": ["project_id", "service_id", "image"]
                }
            },
            {
                "name": "get_deployment_logs",
                "description": "Get logs from a deployment",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "deployment_id": {
                            "type": "string",
                            "description": "Deployment ID"
                        }
                    },
                    "required": ["deployment_id"]
                }
            }
        ]
    
    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a deployment tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            if name == "list_deployments":
                project_id = arguments.get("project_id")
                deployments = await self.client.list_deployments(project_id)
                return {
                    "success": True,
                    "data": deployments,
                    "message": f"Found {len(deployments)} deployments"
                }
            
            elif name == "get_deployment":
                deployment_id = arguments.get("deployment_id")
                deployment = await self.client.get_deployment(deployment_id)
                return {
                    "success": True,
                    "data": deployment,
                    "message": f"Deployment {deployment_id} retrieved"
                }
            
            elif name == "create_deployment":
                project_id = arguments.get("project_id")
                service_id = arguments.get("service_id")
                image = arguments.get("image")
                config = arguments.get("config", {})
                
                deployment = await self.client.create_deployment(
                    project_id=project_id,
                    service_id=service_id,
                    image=image,
                    config=config
                )
                return {
                    "success": True,
                    "data": deployment,
                    "message": f"Deployment created successfully for service {service_id}"
                }
            
            elif name == "get_deployment_logs":
                deployment_id = arguments.get("deployment_id")
                logs = await self.client.get_deployment_logs(deployment_id)
                return {
                    "success": True,
                    "data": logs,
                    "message": f"Retrieved {len(logs)} log lines for deployment {deployment_id}"
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {name}"
                }
        
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
