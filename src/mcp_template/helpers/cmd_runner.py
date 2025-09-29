import subprocess
import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from . import logger


class CommandError(Exception):
    """Custom exception for command execution errors."""

    def __init__(self, message: str, cmd: List[str], returncode: int, stderr: str = ""):
        self.message = message
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(message)


async def run_command(
    cmd: List[str],
    *,
    timeout: Optional[float] = 30.0,
    check: bool = True,
    parse_json: bool = False,
    log_errors: bool = True,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    ctx: Optional[Context[ServerSession, Any]] = None,
) -> Union[str, Dict[str, Any], List[Any]]:
    """
    Run a command with comprehensive error handling and optional JSON parsing.

    Args:
        cmd: Command and arguments as a list
        timeout: Command timeout in seconds (default: 30.0)
        check: Whether to raise exception on non-zero exit code (default: True)
        parse_json: Whether to parse stdout as JSON (default: False)
        log_errors: Whether to log errors (default: True)
        cwd: Working directory for the command
        env: Environment variables for the command

    Returns:
        Command stdout as string, or parsed JSON if parse_json=True

    Raises:
        CommandError: If command fails and check=True
    """
    cmd_str = " ".join(cmd)
    await logger.debug(f"Running command: {cmd_str}", component="cmd_runner", ctx=ctx)

    try:
        # Run command in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,  # We'll handle check ourselves
                cwd=cwd,
                env=env,
            ),
        )

        # Handle non-zero exit codes
        if result.returncode != 0 and check:
            error_msg = f"Command failed with exit code {result.returncode}: {cmd_str}"
            if result.stderr:
                error_msg += f"\nStderr: {result.stderr.strip()}"

            if log_errors:
                await logger.error(error_msg, component="cmd_runner", ctx=ctx)

            raise CommandError(
                message=error_msg, cmd=cmd, returncode=result.returncode, stderr=result.stderr
            )

        # Parse JSON if requested
        if parse_json and result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse command output as JSON: {str(e)}"
                if log_errors:
                    await logger.error(
                        f"{error_msg}\nCommand: {cmd_str}\nOutput: {result.stdout[:500]}...",
                        component="cmd_runner",
                        ctx=ctx,
                    )
                raise CommandError(
                    message=error_msg, cmd=cmd, returncode=result.returncode, stderr=str(e)
                )

        await logger.debug(
            f"Command completed successfully: {cmd_str}", component="cmd_runner", ctx=ctx
        )
        return result.stdout

    except subprocess.TimeoutExpired as e:
        error_msg = f"Command timed out after {timeout}s: {cmd_str}"
        if log_errors:
            await logger.error(error_msg, component="cmd_runner", ctx=ctx)
        raise CommandError(message=error_msg, cmd=cmd, returncode=-1, stderr="Command timed out")
    except Exception as e:
        error_msg = f"Unexpected error running command: {cmd_str} - {str(e)}"
        if log_errors:
            await logger.error(error_msg, component="cmd_runner", ctx=ctx)
        raise CommandError(message=error_msg, cmd=cmd, returncode=-1, stderr=str(e))


async def run_kubectl_command(
    args: List[str],
    *,
    context: Optional[str] = None,
    namespace: Optional[str] = None,
    output_format: str = "json",
    ctx: Optional[Context[ServerSession, Any]] = None,
    **kwargs,
) -> Union[str, Dict[str, Any], List[Any]]:
    """
    Run a kubectl command with common options.

    Args:
        args: kubectl arguments (without 'kubectl' prefix)
        context: Kubernetes context to use
        namespace: Kubernetes namespace to use
        output_format: Output format (json, yaml, etc.)
        **kwargs: Additional arguments passed to run_command

    Returns:
        Command output, parsed as JSON if output_format is 'json'
    """
    if "kubectl" not in args:
        cmd = ["kubectl"] + args
    else:
        cmd = args

    # Add context if specified
    if context:
        cmd.extend(["--context", context])

    # Add namespace if specified
    if namespace:
        cmd.extend(["--namespace", namespace])

    # Add output format if not already specified
    if output_format and not any(arg.startswith(("-o", "--output")) for arg in args):
        cmd.extend(["--output", output_format])

    # Parse JSON by default if output format is json
    parse_json = kwargs.pop("parse_json", output_format == "json")

    return await run_command(cmd, parse_json=parse_json, ctx=ctx, **kwargs)
