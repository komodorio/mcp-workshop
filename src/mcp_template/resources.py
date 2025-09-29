"""
Resources implementation for MCP server.

This is where you define your resources. Users mainly need to modify this file.
"""

from mcp.server.fastmcp import FastMCP
from .helpers import logger


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the FastMCP server."""
