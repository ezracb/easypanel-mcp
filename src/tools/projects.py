"""
Projects Tool Module.

Provides tools for managing EasyPanel projects.
"""

import logging
from typing import Any
from src.client import EasyPanelClient

logger = logging.getLogger(__name__)


class ProjectsTools:
    """Tools for managing projects in EasyPanel."""
    
    def __init__(self, client: EasyPanelClient):
        """
        Initialize projects tools.
        
        Args:
            client: EasyPanel API client
        """
        self.client = client
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """
        Get MCP tool definitions for projects.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "list_projects",
                "description": "List all projects in EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_project",
                "description": "Get detailed information about a specific project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        }
                    },
                    "required": ["project_id"]
                }
            },
            {
                "name": "create_project",
                "description": "Create a new project in EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Project name"
                        },
                        "description": {
                            "type": "string",
                            "description": "Project description"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "delete_project",
                "description": "Delete a project from EasyPanel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        }
                    },
                    "required": ["project_id"]
                }
            },
            {
                "name": "trpc_call",
                "description": "Call a raw tRPC procedure (DEBUG only)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "procedure": {
                            "type": "string",
                            "description": "Procedure name"
                        },
                        "input": {
                            "type": "object",
                            "description": "Input parameters"
                        }
                    },
                    "required": ["procedure"]
                }
            }
        ]
    
    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a project tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            if name == "list_projects":
                projects = await self.client.list_projects()
                return {
                    "success": True,
                    "data": projects,
                    "message": f"Found {len(projects)} projects"
                }
            
            elif name == "get_project":
                project_id = arguments.get("project_id")
                project = await self.client.get_project(project_id)
                return {
                    "success": True,
                    "data": project,
                    "message": f"Project {project_id} retrieved"
                }
            
            elif name == "create_project":
                name_param = arguments.get("name")
                description = arguments.get("description")
                
                project = await self.client.create_project(
                    name=name_param,
                    description=description
                )
                return {
                    "success": True,
                    "data": project,
                    "message": f"Project '{name_param}' created successfully"
                }
            
            elif name == "delete_project":
                project_id = arguments.get("project_id")
                result = await self.client.delete_project(project_id)
                return {
                    "success": True,
                    "data": result,
                    "message": f"Project {project_id} deleted successfully"
                }
            
            elif name == "trpc_call":
                procedure = arguments.get("procedure")
                input_data = arguments.get("input")
                return await self.client._trpc_request(procedure, input_data)
            
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
