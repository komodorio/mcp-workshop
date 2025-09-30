"""Simple E2E tests for FastMCP server."""

import pytest

from mcp_template.server import create_server


def test_fastmcp_server_creation():
    """Test that the FastMCP server can be created."""
    server = create_server()
    assert server is not None
    assert server.name == "mcp-server"


@pytest.mark.asyncio
async def test_server_tool_registration():
    """Test that tools are properly registered."""
    server = create_server()

    # Check tools are available via the public API
    tools = await server.list_tools()
    tool_names = {tool.name for tool in tools}
    expected_tools = {
        "kubectl",
        "base64",
    }
    assert expected_tools.issubset(tool_names)


@pytest.mark.asyncio
async def test_server_prompt_registration():
    """Test that prompts are properly registered."""
    server = create_server()

    # Check prompts are available via the public API
    prompts = await server.list_prompts()
    prompt_names = {prompt.name for prompt in prompts}
    expected_prompts = {
        "diagnose_cluster_issues", 
        "cluster_health_overview", 
        "troubleshoot_workload", 
        "generate_architecture_diagram"
    }
    assert expected_prompts.issubset(prompt_names)


@pytest.mark.asyncio
async def test_server_resource_registration():
    """Test that resources are properly registered."""
    server = create_server()

    # Check resources are available via the public API
    resources = await server.list_resources()
    resource_uris = {str(resource.uri) for resource in resources}
    expected_resources = {"kubectl://contexts"}
    assert expected_resources.issubset(resource_uris)


# Note: More comprehensive E2E tests would require setting up actual MCP client connections
# For now, these basic tests ensure the server structure is correct
