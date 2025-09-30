"""
Tools implementation for MCP server.

This is where you define your tools. Users mainly need to modify this file.
"""

import base64 as b64
from typing import Any, Literal

from mcp.server.elicitation import AcceptedElicitation, CancelledElicitation, DeclinedElicitation
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel

from .helpers import logger
from .helpers.cmd_runner import CommandError, run_kubectl_command
from .helpers.k8s import get_default_context
from .helpers.telemetry import tracer

approval_required = False

class ConfirmationSchema(BaseModel):
    """Schema for user confirmation."""

    accept: bool


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the FastMCP server."""

    @mcp.tool()
    @tracer(
        name="tool.kubectl",
        redact_keys={"token", "secret", "password", "key"},
        arg_denylist={"ctx"},
    )
    async def kubectl(
        cmd: str,
        context: str | None = None,
        namespace: str | None = None,
        output_format: str = "json",
        timeout: float = 30.0,
        ctx: Context[ServerSession, Any] = None,
    ) -> str | dict[str, Any] | list[Any]:
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
        if approval_required:
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
                "kubectl command completed successfully", component="kubectl", ctx=ctx
            )

            return result

        except CommandError as e:
            await logger.error(
                f"kubectl command failed: {e.message}",
                component="kubectl",
                ctx=ctx,
            )
            raise

    @mcp.tool()
    @tracer(name="tool.base64")
    async def base64(
        text: str,
        action: Literal["encode", "decode"],
        encoding: str = "utf-8",
        ctx: Context[ServerSession, Any] = None,
    ) -> str:
        """Encode or decode base64 text.

        Args:
            text: The text to encode or base64 string to decode
            action: Action to perform - "encode" or "decode"
            encoding: Text encoding to use (default: utf-8)

        Returns:
            Encoded or decoded string based on action

        Examples:
            base64("Hello World", "encode") -> "SGVsbG8gV29ybGQ="
            base64("SGVsbG8gV29ybGQ=", "decode") -> "Hello World"
            base64("Hello 世界", "encode", "utf-8") -> "SGVsbG8g5LiW55WM"
        """
        if action not in ["encode", "decode"]:
            error_msg = f"Invalid action '{action}'. Must be 'encode' or 'decode'"
            await logger.error(error_msg, component="base64", ctx=ctx)
            raise ValueError(error_msg)

        try:
            if action == "encode":
                await logger.info(
                    f"Encoding text to base64 (length: {len(text)})",
                    component="base64",
                    ctx=ctx,
                )
                
                encoded_bytes = text.encode(encoding)
                result = b64.b64encode(encoded_bytes).decode('ascii')
                
                await logger.debug(
                    "Base64 encoding completed successfully",
                    component="base64",
                    ctx=ctx,
                )
                
            else:  # decode
                await logger.info(
                    f"Decoding base64 text (length: {len(text)})",
                    component="base64",
                    ctx=ctx,
                )
                
                # Remove any whitespace that might interfere with decoding
                cleaned_text = text.strip()
                
                decoded_bytes = b64.b64decode(cleaned_text)
                result = decoded_bytes.decode(encoding)
                
                await logger.debug(
                    "Base64 decoding completed successfully",
                    component="base64",
                    ctx=ctx,
                )
            
            return result
            
        except UnicodeEncodeError as e:
            error_msg = f"Failed to encode text with {encoding} encoding: {str(e)}"
            await logger.error(error_msg, component="base64", ctx=ctx)
            raise ValueError(error_msg)
        except Exception as e:
            # Handle both base64 decoding errors and unicode decoding errors
            if action == "decode":
                if "Invalid base64-encoded string" in str(e) or "binascii.Error" in str(type(e)):
                    error_msg = f"Invalid base64 string: {str(e)}"
                elif "UnicodeDecodeError" in str(type(e)):
                    error_msg = f"Failed to decode bytes with {encoding} encoding: {str(e)}"
                else:
                    error_msg = f"Base64 decoding failed: {str(e)}"
            else:
                error_msg = f"Base64 encoding failed: {str(e)}"
                
            await logger.error(error_msg, component="base64", ctx=ctx)
            raise ValueError(error_msg)
