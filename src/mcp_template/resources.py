"""
Resources implementation for MCP server.

This is where you define your resources. Users mainly need to modify this file.
"""

from mcp.server.fastmcp import FastMCP

from .helpers.k8s import get_cluster_info, get_kubectl_contexts, get_namespaces
from .helpers.telemetry import tracer
from .models import ClusterInfo, ErrorResponse, KubectlContextsResponse, NamespacesResponse


def register_resources(mcp: FastMCP) -> None:
    """Register all resources with the FastMCP server."""

    @mcp.resource("kubectl://contexts")
    @tracer(
        name="resource.kubectl_contexts",
        attribute_prefix="mcp.resource",
    )
    async def kubectl_contexts() -> KubectlContextsResponse | ErrorResponse:
        """List all available kubectl contexts."""
        try:
            contexts = await get_kubectl_contexts(ctx=mcp.get_context())
            return contexts
        except Exception as e:
            return ErrorResponse(error=f"Error getting kubectl contexts: {str(e)}")

    @mcp.resource("kubectl://cluster-info/{context}")
    @tracer(
        name="resource.kubectl_cluster_info",
        attribute_prefix="mcp.resource",
    )
    async def kubectl_cluster_info(context: str = "default") -> ClusterInfo | ErrorResponse:
        """Get cluster information for specified context."""
        try:
            cluster_info = await get_cluster_info(
                context if context != "default" else None, ctx=mcp.get_context()
            )
            return cluster_info
        except Exception as e:
            return ErrorResponse(
                error=f"Error getting cluster info for context '{context}': {str(e)}",
                context=context,
            )

    @mcp.resource("kubectl://namespaces/{context}")
    @tracer(
        name="resource.kubectl_namespaces",
        attribute_prefix="mcp.resource",
    )
    async def kubectl_namespaces_context(context: str) -> NamespacesResponse | ErrorResponse:
        """List all namespaces in the specified context."""
        try:
            namespaces = await get_namespaces(
                context if context != "default" else None, ctx=mcp.get_context()
            )
            return namespaces
        except Exception as e:
            return ErrorResponse(
                error=f"Error getting namespaces for context '{context}': {str(e)}", context=context
            )
