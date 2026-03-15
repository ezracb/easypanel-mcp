"""
Services Tool Module.

Provides tools for managing EasyPanel services.
"""

import logging
from typing import Any
from src.client import EasyPanelClient

logger = logging.getLogger(__name__)


class ServicesTools:
    """Tools for managing services in EasyPanel."""
    
    def __init__(self, client: EasyPanelClient):
        """
        Initialize services tools.
        
        Args:
            client: EasyPanel API client
        """
        self.client = client
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """
        Get MCP tool definitions for services.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "list_services",
                "description": "List all services in EasyPanel, optionally filtered by project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Optional project ID to filter services"
                        }
                    }
                }
            },
            {
                "name": "get_service",
                "description": "Get detailed information about a specific service",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        }
                    },
                    "required": ["service_id"]
                }
            },
            {
                "name": "create_service",
                "description": "Create a new service in EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Service name"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "image": {
                            "type": "string",
                            "description": "Docker image (e.g., nginx:latest, postgres:15)"
                        },
                        "config": {
                            "type": "object",
                            "description": "Additional configuration (ports, env vars, volumes, etc.)"
                        }
                    },
                    "required": ["name", "project_id", "image"]
                }
            },
            {
                "name": "update_service",
                "description": "Update service configuration",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        },
                        "config": {
                            "type": "object",
                            "description": "New configuration settings"
                        }
                    },
                    "required": ["service_id", "config"]
                }
            },
            {
                "name": "delete_service",
                "description": "Delete a service from EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        }
                    },
                    "required": ["service_id"]
                }
            },
            {
                "name": "restart_service",
                "description": "Restart a service",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        }
                    },
                    "required": ["service_id"]
                }
            },
            {
                "name": "get_service_logs",
                "description": "Get logs from a service",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_id": {
                            "type": "string",
                            "description": "Service ID"
                        },
                        "lines": {
                            "type": "integer",
                            "description": "Number of log lines to retrieve",
                            "default": 100
                        }
                    },
                    "required": ["service_id"]
                }
            }
        ]
    
    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a service tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            if name == "list_services":
                project_id = arguments.get("project_id")
                services = await self.client.list_services(project_id)
                return {
                    "success": True,
                    "data": services,
                    "message": f"Found {len(services)} services"
                }
            
            elif name == "get_service":
                service_id = arguments.get("service_id")
                service = await self.client.get_service(service_id)
                return {
                    "success": True,
                    "data": service,
                    "message": f"Service {service_id} retrieved"
                }
            
            elif name == "create_service":
                name_param = arguments.get("name")
                project_id = arguments.get("project_id")
                image = arguments.get("image")
                config = arguments.get("config", {})
                
                service = await self.client.create_service(
                    name=name_param,
                    project_id=project_id,
                    image=image,
                    config=config
                )
                return {
                    "success": True,
                    "data": service,
                    "message": f"Service '{name_param}' created successfully"
                }
            
            elif name == "update_service":
                service_id = arguments.get("service_id")
                config = arguments.get("config")
                
                service = await self.client.update_service(service_id, config)
                return {
                    "success": True,
                    "data": service,
                    "message": f"Service {service_id} updated successfully"
                }
            
            elif name == "delete_service":
                service_id = arguments.get("service_id")
                result = await self.client.delete_service(service_id)
                return {
                    "success": True,
                    "data": result,
                    "message": f"Service {service_id} deleted successfully"
                }
            
            elif name == "restart_service":
                service_id = arguments.get("service_id")
                result = await self.client.restart_service(service_id)
                return {
                    "success": True,
                    "data": result,
                    "message": f"Service {service_id} restarted successfully"
                }
            
            elif name == "get_service_logs":
                service_id = arguments.get("service_id")
                lines = arguments.get("lines", 100)
                
                logs = await self.client.get_service_logs(service_id, lines)
                return {
                    "success": True,
                    "data": logs,
                    "message": f"Retrieved {len(logs)} log lines for service {service_id}"
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
