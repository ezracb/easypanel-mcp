"""
EasyPanel MCP Server.

Low-level implementation using mcp.server.Server for maximum control.
Supports SSE and STDIO transports.
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
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.client: Optional[EasyPanelClient] = None
        self.tools: dict[str, Any] = {}
        self.mcp_server = Server("easypanel-remote")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.mcp_server.list_tools()
        async def handle_list_tools() -> list:
            definitions = []
            for tool_module in self.tools.values():
                definitions.extend(tool_module.get_tool_definitions())
            
            from mcp.types import Tool
            return [
                Tool(
                    name=t["name"],
                    description=t["description"],
                    inputSchema=t["inputSchema"]
                ) for t in definitions
            ]

        @self.mcp_server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> list:
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
        config.validate()
        self.client = EasyPanelClient(config.easypanel)
        await self.client.connect()
        self.tools = {
            "services": ServicesTools(self.client),
            "deployments": DeploymentsTools(self.client),
            "networks": NetworksTools(self.client),
            "projects": ProjectsTools(self.client)
        }
        logger.info("Server initialized successfully")

    async def run_stdio(self) -> None:
        await self.initialize()
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await self.mcp_server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="easypanel-remote",
                    server_version="1.0.0",
                    capabilities=self.mcp_server.get_capabilities(
                        notification_options=InitializationOptions().capabilities.notifications,
                        experimental_capabilities=InitializationOptions().capabilities.experimental,
                    ),
                ),
            )

    async def run_sse(self, host: str, port: int) -> None:
        await self.initialize()
        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
                await self.mcp_server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="easypanel-remote",
                        server_version="1.0.0",
                        capabilities=self.mcp_server.get_capabilities(
                            notification_options=InitializationOptions().capabilities.notifications,
                            experimental_capabilities=InitializationOptions().capabilities.experimental,
                        ),
                    ),
                )

        app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages", app=sse.handle_post_message),
            ],
        )
        
        logger.info(f"Starting MCP server on SSE at {host}:{port}")
        config_uvicorn = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config_uvicorn)
        await server.serve()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    server = MCPServer()
    if len(sys.argv) > 1 and sys.argv[1] in ["http", "sse"]:
        asyncio.run(server.run_sse(host, port))
    else:
        asyncio.run(server.run_stdio())
