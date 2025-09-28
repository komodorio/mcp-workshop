"""
Resources implementation for MCP server.

This is where you define your resources. Users mainly need to modify this file.
"""

import json
from typing import Any
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from .helpers.k8s import get_kubectl_contexts, get_cluster_info, get_namespaces


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the FastMCP server."""

    @mcp.resource("kubectl://contexts")
    async def kubectl_contexts() -> str:
        """List all available kubectl contexts."""
        try:
            contexts = await get_kubectl_contexts(ctx=mcp.get_context())
            return json.dumps(contexts, indent=2)
        except Exception as e:
            return f"Error getting kubectl contexts: {str(e)}"

    @mcp.resource("kubectl://cluster-info/{context}")
    async def kubectl_cluster_info(context: str = "default") -> str:
        """Get cluster information for specified context."""
        try:
            cluster_info = await get_cluster_info(
                context if context != "default" else None, ctx=mcp.get_context()
            )
            return json.dumps(cluster_info, indent=2)
        except Exception as e:
            return f"Error getting cluster info for context '{context}': {str(e)}"

    @mcp.resource("kubectl://namespaces/{context}")
    async def kubectl_namespaces_context(context: str) -> str:
        """List all namespaces in the specified context."""
        try:
            namespaces = await get_namespaces(
                context if context != "default" else None, ctx=mcp.get_context()
            )
            return json.dumps(namespaces, indent=2)
        except Exception as e:
            return f"Error getting namespaces for context '{context}': {str(e)}"
