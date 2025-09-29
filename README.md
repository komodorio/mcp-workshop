# MCP Server Template

A clean, simple template for creating MCP (Model Context Protocol) servers in Python using FastMCP.

## 🚀 Features

- ✅ **FastMCP Framework** - Simple decorator-based API
- ✅ **Complete MCP Support** - Prompts, Tools, and Resources
- ✅ **Context Logging** - Proper logging through MCP context
- ✅ **Input Validation** - Safe input handling and sanitization
- ✅ **Comprehensive Testing** - Unit tests with pytest
- ✅ **Production Ready** - Clean, maintainable code structure

## 🎯 What's Included

### Tools

- **echo** - Basic tool demonstrating input validation and logging
- **advanced_calculator** - Advanced tool with progress tracking and structured logging

### Prompts

- **hello_world** - Simple greeting prompt
- **code_review** - Code review prompt generator

### Resources

- **server://info** - Server information and metadata
- **server://status** - Current server status and metrics

## 🚀 Quick Start

1. **Install dependencies:**

   ```bash
   uv sync
   ```

2. **Run the server:**

   ```bash
   # stdio transport (default)
   uv run python -m mcp_template.main

   # SSE transport
   uv run python -m mcp_template.main --transport sse --port 8000

   # HTTP transport
   uv run python -m mcp_template.main --transport http --port 8000
   ```

3. **Test with MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector uv run python -m mcp_template.main
   ```

## 🧪 Testing

Run the test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src/mcp_template --cov-report=html
```

## 📁 Project Structure

```
src/mcp_template/
├── __init__.py          # Package initialization
├── main.py              # CLI entry point with transport options
├── server.py            # FastMCP server setup
├── tools.py             # Tool implementations (your main work area)
├── prompts.py           # Prompt implementations
├── resources.py         # Resource implementations
└── helpers/
    ├── __init__.py      # Helper exports
    ├── logging.py       # MCP context logger
    └── validation.py    # Input validation utilities
```

## 🛠️ Development

### Adding New Tools

Edit `src/mcp_template/tools.py`:

```python
@mcp.tool()
async def my_tool(input_data: str, ctx: Context[ServerSession, Any] = None) -> str:
    """My custom tool."""
    if ctx:
        logger = Logger(ctx, "my_tool")
        await logger.info("Tool started")

    # Your logic here
    result = f"Processed: {input_data}"

    if ctx:
        await logger.info("Tool completed")

    return result
```

### Adding New Prompts

Edit `src/mcp_template/prompts.py`:

```python
@mcp.prompt()
def my_prompt(topic: str, style: str = "professional") -> str:
    """Generate a prompt about a topic."""
    return f"Write about {topic} in a {style} style..."
```

### Adding New Resources

Edit `src/mcp_template/resources.py`:

```python
@mcp.resource("my://resource")
def my_resource() -> str:
    """My custom resource."""
    return json.dumps({"message": "Hello from my resource"})
```

## 🔧 Configuration

The server uses FastMCP's automatic configuration. For custom settings, modify `src/mcp_template/server.py`.

## 📝 Logging

The template includes a Logger class that sends messages to MCP clients using the [official MCP logging approach](https://github.com/modelcontextprotocol/python-sdk):

```python
from .helpers import Logger

# In your tool function
if ctx:
    logger = Logger(ctx, "component_name")
    await logger.info("Processing started", extra={"user_id": 123})
    await logger.debug("Debug information")
    await logger.warning("Warning message")
    await logger.error("Error occurred", extra={"error_code": "E001"})
```

The Logger automatically formats messages with component names and handles structured logging with extra data. It gracefully handles test environments where context may not be available.

## 🚀 Deployment

For production deployment:

1. Build with uv:

   ```bash
   uv build
   ```

2. Install the built package:

   ```bash
   pip install dist/mcp_template-*.whl
   ```

3. Run:
   ```bash
   python -m mcp_template.main
   ```

## 📚 FastMCP Documentation

For more information about FastMCP features, visit:

- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
