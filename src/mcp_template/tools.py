"""
Tools implementation for MCP server.

This is where you define your tools. Users mainly need to modify this file.
"""

from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.server.elicitation import AcceptedElicitation, DeclinedElicitation, CancelledElicitation
from pydantic import BaseModel
from .helpers import logger
from .helpers.cmd_runner import run_kubectl_command, CommandError
from .helpers.k8s import get_default_context


class ConfirmationSchema(BaseModel):
    """Schema for user confirmation."""

    accept: bool


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the FastMCP server."""

    @mcp.tool()
    async def kubectl(
        cmd: str,
        context: Optional[str] = None,
        namespace: Optional[str] = None,
        output_format: str = "json",
        timeout: float = 30.0,
        ctx: Context[ServerSession, Any] = None,
    ) -> Union[str, Dict[str, Any], List[Any]]:
        """Execute kubectl commands with comprehensive error handling.

        Dangerous commands (delete, apply, create, etc.) will prompt for user confirmation
        before execution to prevent accidental cluster modifications.

        Args:
            cmd: kubectl command as a string (without 'kubectl' prefix)
            context: Kubernetes context to use (default: current context from kubectl config)
            namespace: Kubernetes namespace to use (default: "default")
            output_format: Output format (json, yaml, table, etc.)
            timeout: Command timeout in seconds (default: 30.0)

        Returns:
            Command output, parsed as JSON if output_format is 'json'

        Examples:
            kubectl("get pods") - Get all pods in JSON format (no confirmation)
            kubectl("get pods", namespace="kube-system", output_format="table")
            kubectl("describe pod my-pod", context="my-cluster")
            kubectl("logs deployment/my-app --tail=100")
            kubectl("apply -f deployment.yaml") - Will ask for confirmation
            kubectl("delete pod my-pod") - Will ask for confirmation
        """
        args = cmd.split(" ")

        # Get the actual current context if not specified
        if context is None:
            context = await get_default_context(ctx=ctx)

        # Check if this is a potentially dangerous command that requires confirmation
        dangerous_commands = {
            "delete",
            "apply",
            "create",
            "replace",
            "patch",
            "edit",
            "scale",
            "rollout",
            "drain",
            "cordon",
            "uncordon",
            "taint",
        }

        if args and args[0].lower() in dangerous_commands:
            await logger.warning(
                f"Dangerous kubectl command detected: {' '.join(args)}",
                component="kubectl",
                ctx=ctx,
            )

            # Request user confirmation for dangerous operations
            confirmation = await ctx.elicit(
                f"⚠️  This command may modify cluster state: `kubectl {cmd}`\n\nDo you want to proceed?",
                ConfirmationSchema,
            )

            match confirmation:
                case AcceptedElicitation(data=response):
                    if response.accept:
                        await logger.info(
                            f"User confirmed dangerous command: {' '.join(args)}",
                            component="kubectl",
                            ctx=ctx,
                        )
                    else:
                        await logger.info(
                            f"User rejected dangerous command: {' '.join(args)}",
                            component="kubectl",
                            ctx=ctx,
                        )
                        return "Command rejected by user"
                case DeclinedElicitation():
                    await logger.info(
                        f"User declined dangerous command: {' '.join(args)}",
                        component="kubectl",
                        ctx=ctx,
                    )
                    return "Command declined by user"
                case CancelledElicitation():
                    await logger.info(
                        f"User cancelled dangerous command: {' '.join(args)}",
                        component="kubectl",
                        ctx=ctx,
                    )
                    return "Command cancelled by user"

        await logger.info(
            f"Executing kubectl command: {' '.join(args)}", component="kubectl", ctx=ctx
        )

        try:
            result = await run_kubectl_command(
                args=args,
                context=context,
                namespace=namespace,
                output_format=output_format,
                timeout=timeout,
                ctx=ctx,
            )

            await logger.debug(
                f"kubectl command completed successfully", component="kubectl", ctx=ctx
            )

            return result

        except CommandError as e:
            await logger.error(
                f"kubectl command failed: {e.message}",
                component="kubectl",
                ctx=ctx,
            )
            raise
