"""
EasyPanel MCP Server.

Main server implementation using the Model Context Protocol (MCP).
Provides AI agents with tools to manage EasyPanel infrastructure.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport

from config import config
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
    """
    
    def __init__(self):
        """Initialize MCP server."""
        self.client: Optional[EasyPanelClient] = None
        self.tools: dict[str, Any] = {}
        self.mcp_server = Server("easypanel-mcp")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP protocol handlers."""
        
        @self.mcp_server.list_tools()
        async def handle_list_tools() -> list:
            """List all available tools."""
            definitions = []
            for tool_module in self.tools.values():
                definitions.extend(tool_module.get_tool_definitions())
            
            # Format according to SDK expectations
            from mcp.types import Tool, TextContent
            return [
                Tool(
                    name=t["name"],
                    description=t["description"],
                    inputSchema=t["inputSchema"]
                ) for t in definitions
            ]

        @self.mcp_server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> list:
            """Execute a tool."""
            # Determine which tool module to use
            tool_module = None
            for module in self.tools.values():
                if any(t["name"] == name for t in module.get_tool_definitions()):
                    tool_module = module
                    break
            
            if not tool_module:
                raise ValueError(f"Unknown tool: {name}")
            
            result = await tool_module.execute(name, arguments or {})
            
            from mcp.types import TextContent
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

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

    async def run_stdio(self) -> None:
        """Run the MCP server using STDIO transport."""
        await self.initialize()
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await self.mcp_server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="easypanel-mcp",
                    server_version="1.0.0",
                    capabilities=self.mcp_server.get_capabilities(
                        notification_options=InitializationOptions().capabilities.notifications,
                        experimental_capabilities=InitializationOptions().capabilities.experimental,
                    ),
                ),
            )

    async def run_sse(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Run the MCP server using SSE transport."""
        await self.initialize()
        
        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_scope(request.scope, request.receive, request._send):
                await self.mcp_server.run(
                    sse.read_stream,
                    sse.write_stream,
                    InitializationOptions(
                        server_name="easypanel-mcp",
                        server_version="1.0.0",
                        capabilities=self.mcp_server.get_capabilities(
                            notification_options=InitializationOptions().capabilities.notifications,
                            experimental_capabilities=InitializationOptions().capabilities.experimental,
                        ),
                    ),
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages", app=sse.handle_post_message),
            ],
        )
        
        logger.info(f"MCP server running on SSE at {host}:{port}")
        
        # Run uvicorn
        config_uvicorn = uvicorn.Config(
            starlette_app, 
            host=host, 
            port=port, 
            log_level="info"
        )
        server = uvicorn.Server(config_uvicorn)
        await server.serve()

if __name__ == "__main__":
    import sys
    
    # Get port from env
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    
    server = MCPServer()
    
    if len(sys.argv) > 1 and sys.argv[1] in ["http", "sse"]:
        asyncio.run(server.run_sse(host=host, port=port))
    else:
        asyncio.run(server.run_stdio())
