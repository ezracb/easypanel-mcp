"""
EasyPanel MCP Server.

Main server implementation using the Model Context Protocol (MCP).
Provides AI agents with tools to manage EasyPanel infrastructure.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Optional

from config import config, Config
from src.client import EasyPanelClient
from src.tools import (
    ServicesTools,
    DeploymentsTools,
    NetworksTools,
    ProjectsTools
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.server.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server for EasyPanel.
    
    Implements the Model Context Protocol to expose EasyPanel
    functionality to AI agents.
    """
    
    def __init__(self):
        """Initialize MCP server."""
        self.client: Optional[EasyPanelClient] = None
        self.tools: dict[str, Any] = {}
        self._running = False
    
    async def initialize(self) -> None:
        """Initialize server and connect to EasyPanel."""
        logger.info("Initializing EasyPanel MCP Server...")
        
        # Validate configuration
        config.validate()
        
        # Initialize EasyPanel client
        self.client = EasyPanelClient(config.easypanel)
        await self.client.connect()
        
        # Initialize tools
        self.tools = {
            "services": ServicesTools(self.client),
            "deployments": DeploymentsTools(self.client),
            "networks": NetworksTools(self.client),
            "projects": ProjectsTools(self.client)
        }
        
        logger.info("Server initialized successfully")
    
    async def shutdown(self) -> None:
        """Shutdown server and disconnect from EasyPanel."""
        logger.info("Shutting down server...")
        self._running = False
        if self.client:
            await self.client.disconnect()
        logger.info("Server shutdown complete")
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """
        Get all tool definitions.
        
        Returns:
            List of all tool definitions
        """
        definitions = []
        for tool_module in self.tools.values():
            definitions.extend(tool_module.get_tool_definitions())
        return definitions
    
    async def execute_tool(
        self,
        name: str,
        arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Execute a tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        # Determine which tool module to use
        tool_module = None
        for module_name, module in self.tools.items():
            tool_defs = module.get_tool_definitions()
            if any(t["name"] == name for t in tool_defs):
                tool_module = module
                break
        
        if not tool_module:
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }
        
        return await tool_module.execute(name, arguments)
    
    async def handle_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Handle incoming MCP message.
        
        Args:
            message: Incoming MCP message
            
        Returns:
            Response message
        """
        method = message.get("method", "")
        params = message.get("params", {})
        msg_id = message.get("id")
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {}
                        },
                        "serverInfo": {
                            "name": "easypanel-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": self.get_tool_definitions()
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                result = await self.execute_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            elif method == "ping":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {}
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    async def run(self) -> None:
        """Run the MCP server (STDIO transport)."""
        await self.initialize()
        self._running = True
        
        logger.info("MCP server running on STDIO")
        
        while self._running:
            try:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                # Parse message
                message = json.loads(line)
                
                # Handle message and send response
                response = await self.handle_message(message)
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                logger.error("Failed to parse message")
            except Exception as e:
                logger.error(f"Error in server loop: {e}")
                if not self._running:
                    break
        
        await self.shutdown()


if __name__ == "__main__":
    server = MCPServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass
