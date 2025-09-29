"""
Pydantic models for MCP server responses.

This module defines structured response models for better schema capabilities.
"""

from typing import Any

from pydantic import BaseModel, Field


class KubectlContext(BaseModel):
    """Model for a kubectl context."""

    name: str = Field(description="Name of the context")
    cluster: str = Field(description="Cluster name")
    user: str = Field(description="User name")
    namespace: str = Field(default="", description="Default namespace")
    current: bool = Field(description="Whether this is the current context")


class KubectlContextsResponse(BaseModel):
    """Response model for kubectl contexts."""

    contexts: list[KubectlContext] = Field(description="List of available contexts")
    total_count: int = Field(description="Total number of contexts")


class ClusterInfo(BaseModel):
    """Model for cluster information."""

    cluster_info: str = Field(description="Raw cluster info output")
    version_info: str = Field(description="Raw version info output")
    context: str = Field(description="Context name used")


class KubernetesNamespace(BaseModel):
    """Model for a Kubernetes namespace."""

    metadata: dict[str, Any] = Field(description="Namespace metadata")
    status: dict[str, Any] | None = Field(default=None, description="Namespace status")

    @property
    def name(self) -> str:
        """Get the namespace name."""
        return self.metadata.get("name", "")

    @property
    def creation_timestamp(self) -> str | None:
        """Get the creation timestamp."""
        return self.metadata.get("creationTimestamp")

    @property
    def phase(self) -> str | None:
        """Get the namespace phase."""
        if self.status:
            return self.status.get("phase")
        return None


class NamespacesResponse(BaseModel):
    """Response model for namespaces."""

    namespaces: list[KubernetesNamespace] = Field(description="List of namespaces")
    total_count: int = Field(description="Total number of namespaces")
    context: str = Field(description="Context used to fetch namespaces")


class ErrorResponse(BaseModel):
    """Model for error responses."""

    error: str = Field(description="Error message")
    context: str | None = Field(default=None, description="Context where error occurred")
    details: dict[str, Any] | None = Field(default=None, description="Additional error details")
