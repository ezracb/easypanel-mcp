"""
EasyPanel MCP Server.

Final stabilized implementation using Starlette lifespan and uvicorn.run.
Ensures the process remains active in containerized environments.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional
from contextlib import asynccontextmanager

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
        logger.info("Initializing MCP Server components...")
        try:
            config.validate()
            self.client = EasyPanelClient(config.easypanel)
            await self.client.connect()
            self.tools = {
                "services": ServicesTools(self.client),
                "deployments": DeploymentsTools(self.client),
                "networks": NetworksTools(self.client),
                "projects": ProjectsTools(self.client)
            }
            logger.info("MCP Server initialization complete")
        except Exception as e:
            logger.exception(f"CRITICAL: Failed to initialize MCP Server: {e}")
            raise

    async def shutdown(self) -> None:
        if self.client:
            await self.client.disconnect()
            logger.info("EasyPanel client disconnected")

    async def run_stdio(self) -> None:
        """Run the server using STDIO transport."""
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

server_instance = MCPServer()
sse_transport = SseServerTransport("/messages")

@asynccontextmanager
async def lifespan(app: Starlette):
    """Manage server lifecycle."""
    try:
        await server_instance.initialize()
        yield
    except Exception as e:
        logger.exception(f"LIFESPAN ERROR: {e}")
        raise
    finally:
        await server_instance.shutdown()

async def handle_sse(request):
    """Handle SSE connection requests."""
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server_instance.mcp_server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="easypanel-remote",
                server_version="1.0.0",
                capabilities=server_instance.mcp_server.get_capabilities(
                    notification_options=InitializationOptions().capabilities.notifications,
                    experimental_capabilities=InitializationOptions().capabilities.experimental,
                ),
            ),
        )

async def health_check(request):
    """Simple health check endpoint."""
    return JSONResponse({"status": "ok", "server": "easypanel-remote"})

# Define the web application
app = Starlette(
    lifespan=lifespan,
    routes=[
        Route("/", endpoint=health_check),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=sse_transport.handle_post_message),
    ],
)

if __name__ == "__main__":
    # Get configuration
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    
    # Check transport mode
    mode = "stdio"
    if len(sys.argv) > 1 and sys.argv[1] in ["http", "sse"]:
        mode = "sse"
    
    if mode == "sse":
        logger.info(f"Starting MCP server on SSE (Host: {host}, Port: {port})")
        try:
            uvicorn.run(app, host=host, port=port, log_level="info")
        except Exception as e:
            logger.exception(f"UVICORN FATAL ERROR: {e}")
            sys.exit(1)
    else:
        logger.info("Starting MCP server on STDIO")
        try:
            asyncio.run(server_instance.run_stdio())
        except Exception as e:
            logger.exception(f"STDIO FATAL ERROR: {e}")
            sys.exit(1)
