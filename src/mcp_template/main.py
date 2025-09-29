#!/usr/bin/env python3
"""Main entry point for the MCP server."""

import sys

import click

from .server import create_server


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "http"]),
    default="stdio",
    help="Transport type to use (default: stdio)",
)
@click.option(
    "--host",
    default="localhost",
    help="Host to bind to for HTTP/SSE transport (default: localhost)",
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port to bind to for HTTP/SSE transport (default: 8000)",
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    help="Enable auto-reload for development (HTTP/SSE transport only)",
)
def main(transport: str, host: str, port: int, reload: bool) -> None:
    """Run the MCP server with the specified transport."""
    # Create the server
    server = create_server()

    try:
        if transport == "stdio":
            if reload:
                click.echo("⚠️  Auto-reload is not supported with stdio transport", err=True)
            click.echo("🚀 Starting MCP server with stdio transport...", err=True)
            server.run()
        elif transport == "sse":
            reload_msg = " (auto-reload enabled)" if reload else ""
            click.echo(
                f"🚀 Starting MCP server with SSE transport on {host}:{port}{reload_msg}...",
                err=True,
            )
            server.run(transport="sse", mount_path="/")
        elif transport == "http":
            reload_msg = " (auto-reload enabled)" if reload else ""
            click.echo(
                f"🚀 Starting MCP server with HTTP transport on {host}:{port}{reload_msg}...",
                err=True,
            )
            server.run(transport="streamable-http")
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped by user", err=True)
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
