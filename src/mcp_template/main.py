#!/usr/bin/env python3
"""Main entry point for the MCP server."""

import sys

import click
import uvicorn

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
def main(transport: str, host: str, port: int) -> None:
    """Run the MCP server with the specified transport."""
    # Create the server
    server = create_server()

    try:
        if transport == "stdio":
            click.echo("🚀 Starting MCP server with stdio transport...", err=True)
            server.run()
        elif transport == "sse":
            click.echo(f"🚀 Starting MCP server with SSE transport on {host}:{port}...", err=True)
            uvicorn.run(server.sse_app(), host=host, port=port)
        elif transport == "http":
            click.echo(f"🚀 Starting MCP server with HTTP transport on {host}:{port}...", err=True)
            uvicorn.run(server.streamable_http_app(), host=host, port=port)
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped by user", err=True)
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
