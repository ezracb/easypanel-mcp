"""
EasyPanel MCP Server.

Main server implementation using FastMCP for robust transport handling.
Provides AI agents with tools to manage EasyPanel infrastructure.
"""

import logging
import os
import sys
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from config import config
from src.client import EasyPanelClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("easypanel-remote")

# Initialize client
client = EasyPanelClient(config.easypanel)

async def ensure_connected():
    """Ensure the client is connected to EasyPanel."""
    if client._client is None:
        logger.info("Connecting to EasyPanel API...")
        await client.connect()

# ========== Projects ==========

@mcp.tool()
async def list_projects() -> list[dict[str, Any]]:
    """List all projects in Easypanel with their basic metadata."""
    await ensure_connected()
    return await client.list_projects()

@mcp.tool()
async def get_project(project_id: str) -> dict[str, Any]:
    """Get detailed information about a specific project."""
    await ensure_connected()
    return await client.get_project(project_id)

@mcp.tool()
async def create_project(name: str, description: Optional[str] = None) -> dict[str, Any]:
    """Create a new project in EasyPanel."""
    await ensure_connected()
    return await client.create_project(name, description)

@mcp.tool()
async def delete_project(project_id: str) -> dict[str, Any]:
    """Delete a project from EasyPanel."""
    await ensure_connected()
    return await client.delete_project(project_id)

# ========== Services ==========

@mcp.tool()
async def list_services(project_id: Optional[str] = None) -> list[dict[str, Any]]:
    """List all services in EasyPanel, optionally filtered by project."""
    await ensure_connected()
    return await client.list_services(project_id)

@mcp.tool()
async def get_service(service_id: str) -> dict[str, Any]:
    """Get detailed information about a specific service."""
    await ensure_connected()
    return await client.get_service(service_id)

@mcp.tool()
async def create_service(name: str, project_id: str, image: str, config: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Create a new service in EasyPanel (app type)."""
    await ensure_connected()
    return await client.create_service(name, project_id, image, config)

@mcp.tool()
async def restart_service(service_id: str) -> dict[str, Any]:
    """Restart a service."""
    await ensure_connected()
    return await client.restart_service(service_id)

@mcp.tool()
async def deploy_service(service_id: str) -> dict[str, Any]:
    """Trigger a redeployment of a specific service."""
    await ensure_connected()
    return await client.deploy_service(service_id)

# ========== Low-level API Access ==========

@mcp.tool()
async def trpc_call(procedure: str, input_data: Optional[dict[str, Any]] = None, method: str = "POST") -> Any:
    """Make a raw tRPC call to the Easypanel API for advanced operations."""
    await ensure_connected()
    return await client._trpc_request(procedure, input_data, method)

if __name__ == "__main__":
    # Get configuration from env
    port = int(os.environ.get("PORT", os.environ.get("MCP_PORT", 8080)))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    
    # Check for transport mode
    transport = "stdio"
    if len(sys.argv) > 1 and sys.argv[1] in ["http", "sse"]:
        transport = "sse"
        
    logger.info(f"Starting MCP server on {transport.upper()} (Host: {host}, Port: {port})")
    mcp.run(transport=transport, host=host, port=port)
