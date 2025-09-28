"""Core MCP server implementation using FastMCP."""

from mcp.server.fastmcp import FastMCP
from . import prompts, resources, tools


def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    # Create FastMCP server with lifespan management
    mcp = FastMCP(name="mcp-server")

    # Register all handlers with the mcp instance
    prompts.register_prompts(mcp)
    tools.register_tools(mcp)
    resources.register_resources(mcp)

    return mcp
