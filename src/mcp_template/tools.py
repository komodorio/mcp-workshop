"""
Tools implementation for MCP server.

This is where you define your tools. Users mainly need to modify this file.
"""

from typing import Any
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from .helpers import logger


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the FastMCP server."""

    @mcp.tool()
    async def echo(text: str, repeat: int = 1, ctx: Context[ServerSession, Any] = None) -> str:
        """Echo back the input text, optionally repeated.

        This demonstrates basic tool functionality with input validation and logging.
        """

        # Use singleton logger (handles initialization and errors internally)
        await logger.info(
            f"Echo called with text='{text[:50]}...', repeat={repeat}", component="echo", ctx=ctx
        )
        await logger.debug(f"Generated {repeat} repetitions", component="echo", ctx=ctx)

        # Generate result
        result = "\n".join([text] * repeat)
        return result

    @mcp.tool()
    async def health_check(ctx: Context[ServerSession, Any] = None) -> str:
        """Health check endpoint for container monitoring.

        Returns server status and basic system information.
        """
        import time
        import platform

        await logger.info("Health check requested", component="health", ctx=ctx)

        health_info = {
            "status": "healthy",
            "timestamp": time.time(),
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "server": "mcp-server",
        }

        return f"Server is healthy: {health_info}"
