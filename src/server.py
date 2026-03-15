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
        
        logger.debug(f"Received method: {method}")
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {
                                "list": True
                            }
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
    
    async def run_stdio(self) -> None:
        """Run server using stdio transport."""
        logger.info("Starting MCP server with stdio transport")
        self._running = True
        
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        
        writer = await asyncio.open_connection(sys.stdout, sys.stdout)
        
        while self._running:
            try:
                line = await reader.readline()
                if not line:
                    break
                
                message = json.loads(line.decode())
                response = await self.handle_message(message)
                
                writer.write(json.dumps(response).encode() + b"\n")
                await writer.drain()
            
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        writer.close()
        await writer.wait_closed()
    
    async def run_http(self) -> None:
        """Run server using HTTP transport."""
        logger.info(f"Starting MCP server with HTTP transport on {config.server.host}:{config.server.port}")
        
        from aiohttp import web
        
        async def handle_request(request: web.Request) -> web.Response:
            try:
                message = await request.json()
                response = await self.handle_message(message)
                return web.json_response(response)
            except Exception as e:
                logger.error(f"HTTP request error: {e}")
                return web.json_response(
                    {"error": str(e)},
                    status=500
                )
        
        app = web.Application()
        app.router.add_post("/mcp", handle_request)
        app.router.add_post("/", handle_request)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(
            runner,
            config.server.host,
            config.server.port
        )
        await site.start()
        
        self._running = True
        
        try:
            while self._running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            await runner.cleanup()


async def main() -> None:
    """Main entry point."""
    server = MCPServer()
    
    try:
        await server.initialize()
        
        # Determine transport mode
        transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
        
        if transport == "http":
            await server.run_http()
        else:
            await server.run_stdio()
    
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        await server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
