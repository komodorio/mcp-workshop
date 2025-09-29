"""
Prompts implementation for MCP server.

This is where you define your prompts. Users mainly need to modify this file.
"""

from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register all prompts with the FastMCP server."""
