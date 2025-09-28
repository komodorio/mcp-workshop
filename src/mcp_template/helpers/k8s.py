import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from .cmd_runner import run_kubectl_command


async def get_kubectl_contexts(
    ctx: Optional[Context[ServerSession, Any]] = None
) -> List[Dict[str, Any]]:
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
                {
                    "name": context_name,
                    "cluster": context_data.get("cluster", ""),
                    "user": context_data.get("user", ""),
                    "namespace": context_data.get("namespace", ""),
                    "current": context_name == current_context,
                }
            )

        return contexts

    except FileNotFoundError:
        return []
    except yaml.YAMLError:
        return []


async def get_cluster_info(
    context: Optional[str] = None, ctx: Optional[Context[ServerSession, Any]] = None
) -> Dict[str, Any]:
    """Get cluster information for specified context or default."""
    # Get cluster info
    cluster_info = await run_kubectl_command(["cluster-info"], context=context, ctx=ctx, output_format=None)

    # Get version info
    version_info = await run_kubectl_command(["version"], context=context, ctx=ctx, output_format=None)

    return {
        "cluster_info": cluster_info,
        "version_info": version_info,
        "context": context or "default",
    }


async def get_namespaces(
    context: Optional[str] = None, ctx: Optional[Context[ServerSession, Any]] = None
) -> List[Dict[str, Any]]:
    """Get list of namespaces in the cluster."""
    namespaces_data = await run_kubectl_command(["get", "namespaces"], context=context, ctx=ctx)
    return namespaces_data.get("items", [])
