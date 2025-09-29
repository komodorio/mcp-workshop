import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from .cmd_runner import run_command, run_kubectl_command
from ..models import KubectlContext, KubectlContextsResponse, ClusterInfo, KubernetesNamespace, NamespacesResponse


async def get_default_context(ctx: Optional[Context[ServerSession, Any]] = None) -> Optional[str]:
    """Get the current default kubectl context.
    
    First tries to get it via kubectl command, then falls back to reading kubeconfig file.
    
    Returns:
        The current context name, or None if unable to determine
    """
  
    # First try using kubectl command
    result = await run_command(
        ["kubectl", "config", "current-context"],
        ctx=ctx,
        log_errors=False,
        check=False
    )
    
    if result and isinstance(result, str):
        current_context = result.strip()
        if current_context:
            return current_context
    
    return None


async def get_kubectl_contexts(
    ctx: Optional[Context[ServerSession, Any]] = None
) -> KubectlContextsResponse:
    """Get list of available kubectl contexts by reading the kubeconfig file."""
    # Get kubeconfig path from environment or default location
    kubeconfig_path = os.environ.get("KUBECONFIG", str(Path.home() / ".kube" / "config"))

    try:
        with open(kubeconfig_path, "r") as f:
            kubeconfig = yaml.safe_load(f)

        contexts = []
        current_context = kubeconfig.get("current-context", "")

        for context_config in kubeconfig.get("contexts", []):
            context_name = context_config.get("name", "")
            context_data = context_config.get("context", {})

            contexts.append(
                KubectlContext(
                    name=context_name,
                    cluster=context_data.get("cluster", ""),
                    user=context_data.get("user", ""),
                    namespace=context_data.get("namespace", ""),
                    current=context_name == current_context,
                )
            )

        return KubectlContextsResponse(contexts=contexts, total_count=len(contexts))

    except FileNotFoundError:
        return KubectlContextsResponse(contexts=[], total_count=0)
    except yaml.YAMLError:
        return KubectlContextsResponse(contexts=[], total_count=0)


async def get_cluster_info(
    context: Optional[str] = None, ctx: Optional[Context[ServerSession, Any]] = None
) -> ClusterInfo:
    """Get cluster information for specified context or default."""
    # Get cluster info
    cluster_info = await run_kubectl_command(["cluster-info"], context=context, ctx=ctx, output_format=None)

    # Get version info
    version_info = await run_kubectl_command(["version"], context=context, ctx=ctx, output_format=None)

    return ClusterInfo(
        cluster_info=cluster_info,
        version_info=version_info,
        context=context or "default",
    )


async def get_namespaces(
    context: Optional[str] = None, ctx: Optional[Context[ServerSession, Any]] = None
) -> NamespacesResponse:
    """Get list of namespaces in the cluster."""
    namespaces_data = await run_kubectl_command(["get", "namespaces"], context=context, ctx=ctx)
    namespace_items = namespaces_data.get("items", [])
    
    namespaces = [KubernetesNamespace(**item) for item in namespace_items]
    
    return NamespacesResponse(
        namespaces=namespaces,
        total_count=len(namespaces),
        context=context or "default"
    )
