"""
Networks Tool Module.

Provides tools for managing EasyPanel networks.
"""

import logging
from typing import Any
from src.client import EasyPanelClient

logger = logging.getLogger(__name__)


class NetworksTools:
    """Tools for managing networks in EasyPanel."""
    
    def __init__(self, client: EasyPanelClient):
        """
        Initialize networks tools.
        
        Args:
            client: EasyPanel API client
        """
        self.client = client
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """
        Get MCP tool definitions for networks.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "list_networks",
                "description": "List all networks in EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "create_network",
                "description": "Create a new network in EasyPanel. Use internal=true for isolated networks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Network name"
                        },
                        "internal": {
                            "type": "boolean",
                            "description": "Whether the network is internal (isolated from internet)",
                            "default": False
                        },
                        "driver": {
                            "type": "string",
                            "description": "Network driver (overlay, bridge, etc.)",
                            "default": "overlay"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "delete_network",
                "description": "Delete a network from EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "network_id": {
                            "type": "string",
                            "description": "Network ID"
                        }
                    },
                    "required": ["network_id"]
                }
            }
        ]
    
    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a network tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            if name == "list_networks":
                networks = await self.client.list_networks()
                return {
                    "success": True,
                    "data": networks,
                    "message": f"Found {len(networks)} networks"
                }
            
            elif name == "create_network":
                name_param = arguments.get("name")
                internal = arguments.get("internal", False)
                driver = arguments.get("driver", "overlay")
                
                network = await self.client.create_network(
                    name=name_param,
                    internal=internal,
                    driver=driver
                )
                network_type = "internal (isolated)" if internal else "public"
                return {
                    "success": True,
                    "data": network,
                    "message": f"Network '{name_param}' created as {network_type} network"
                }
            
            elif name == "delete_network":
                network_id = arguments.get("network_id")
                result = await self.client.delete_network(network_id)
                return {
                    "success": True,
                    "data": result,
                    "message": f"Network {network_id} deleted successfully"
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
