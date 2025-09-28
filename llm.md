# MCP Server Documentation

## 📋 Kubernetes Resources

The MCP server provides resources to interact with Kubernetes clusters using kubectl:

### Command Runner Utility

The project includes a reusable command runner (`helpers/cmd_runner.py`) with the following features:

- **Async execution**: Non-blocking command execution using thread pools
- **Comprehensive error handling**: Custom `CommandError` exception with detailed context
- **JSON parsing**: Automatic JSON parsing with error handling
- **Timeout support**: Configurable command timeouts (default: 30s)
- **Logging integration**: Automatic error logging with debug information
- **kubectl helper**: Specialized `run_kubectl_command` function with context/namespace support

#### Usage Examples:

```python
from .helpers.cmd_runner import run_command, run_kubectl_command, CommandError

# Generic command execution with MCP context
result = await run_command(["ls", "-la"], timeout=10.0, parse_json=False, ctx=ctx)

# kubectl command with context and namespace
pods = await run_kubectl_command(["get", "pods"], context="production", namespace="default", ctx=ctx)

# Command with custom error handling
try:
    data = await run_command(["some-command"], parse_json=True, ctx=ctx)
except CommandError as e:
    await logger.error(f"Command failed: {e.message}", ctx=ctx)
    print(f"Exit code: {e.returncode}")
```

### Available Resources

1. **`kubectl/contexts`** - List all available kubectl contexts
   - Returns: JSON array of all configured kubectl contexts
   - Usage: Get overview of all available clusters/contexts

2. **`kubectl/cluster-info/{context}`** - Get cluster information for specified context
   - Parameters: `context` (optional, defaults to "default")
   - Returns: JSON object with cluster info and version details
   - Usage: Get detailed information about a specific cluster

3. **`kubectl/namespaces`** - List namespaces in current cluster
   - Returns: JSON array of all namespaces in the current context
   - Usage: Get all namespaces from the default cluster

4. **`kubectl/namespaces/{context}`** - List namespaces for specific context
   - Parameters: `context` (required)
   - Returns: JSON array of all namespaces in the specified context
   - Usage: Get namespaces from a specific cluster context

### Prerequisites

- `kubectl` must be installed and configured
- Valid kubeconfig with access to desired clusters
- Appropriate RBAC permissions for cluster operations

### Example Usage

```bash
# List all contexts
curl http://localhost:8000/resources/kubectl/contexts

# Get cluster info for default context
curl http://localhost:8000/resources/kubectl/cluster-info/default

# Get cluster info for specific context
curl http://localhost:8000/resources/kubectl/cluster-info/production

# List namespaces in default cluster
curl http://localhost:8000/resources/kubectl/namespaces

# List namespaces in specific context
curl http://localhost:8000/resources/kubectl/namespaces/staging
```

## 🐳 Docker Setup

The MCP server has been fully dockerized with production-ready configuration and development support.

### Quick Start

1. **Build the Docker image:**
   ```bash
   make docker-build
   ```

2. **Run the container:**
   ```bash
   # HTTP transport (default, port 8000)
   make docker-run
   
   # STDIO transport (for direct communication)
   make docker-run-stdio
   
   # SSE transport (Server-Sent Events)
   make docker-run-sse
   ```

3. **Stop and clean up:**
   ```bash
   # Stop running container
   make docker-stop
   
   # Clean up Docker artifacts
   make docker-clean
   ```

### Docker Files Overview

- **`Dockerfile`** - Production-ready image with security best practices
- **`.dockerignore`** - Optimized build context exclusions
- **`Makefile`** - Docker commands integrated into the build system

### Transport Modes

The MCP server supports three transport modes:

1. **HTTP Transport** (Default for containers)
   - Best for web integrations and REST APIs
   - Accessible via HTTP requests
   - Port: 8000 (configurable)

2. **SSE Transport** 
   - Server-Sent Events for real-time communication
   - Ideal for streaming applications
   - Port: 8000 (configurable)

3. **STDIO Transport**
   - Standard input/output communication
   - Best for direct process communication
   - No network port required

### Environment Configuration

The container supports these environment variables:

- `PYTHONUNBUFFERED=1` - Ensures immediate output flushing
- `PYTHONDONTWRITEBYTECODE=1` - Prevents .pyc file creation
- Custom environment variables can be added via docker-compose.yml

### Health Monitoring

- **Health Check Tool**: Built-in `health_check` tool for monitoring
- **Docker Health Check**: Automatic container health monitoring
- **Port Check**: Simple socket-based connectivity verification

### Development Workflow

1. **Build and Test:**
   ```bash
   # Build the Docker image
   make docker-build
   
   # Test different transport modes
   make docker-run-stdio
   make docker-run-sse
   make docker-run  # HTTP transport
   ```

2. **Development Cycle:**
   ```bash
   # Make code changes, then rebuild and test
   make docker-build
   make docker-run
   
   # Clean up when done
   make docker-clean
   ```

### Production Deployment

The Docker setup is production-ready with:

- **Security**: Non-root user, minimal attack surface
- **Performance**: Optimized Python environment with uv
- **Monitoring**: Health checks and proper logging
- **Scalability**: Stateless design, easy horizontal scaling

### Troubleshooting

**Container won't start:**
- Check if port 8000 is available: `lsof -i :8000`
- Verify Docker daemon is running: `docker info`
- Check logs: `docker logs mcp-server`

**Build issues:**
- Ensure uv.lock is up to date: `uv lock`
- Verify all source files are present
- Check Dockerfile syntax

**Runtime issues:**
- Verify server is binding to 0.0.0.0, not localhost
- Check if the application started successfully
- Review container logs for startup errors

### Advanced Usage

**Custom Dockerfile modifications:**
- Base image can be changed (currently python:3.11-slim)
- Additional system packages can be added to apt-get install
- Environment variables can be customized

**Scaling with Docker Swarm:**
```bash
docker service create --name mcp-server --replicas 3 -p 8000:8000 mcp-server:latest
```

**Integration with orchestrators:**
- Kubernetes manifests can be created for the Docker image
- Health check tool ready for load balancer integration
- Stateless design supports auto-scaling

**Available Make Commands:**
```bash
make help                # Show all available commands
make docker-build        # Build Docker image
make docker-run          # Run with HTTP transport
make docker-run-stdio    # Run with STDIO transport
make docker-run-sse      # Run with SSE transport
make docker-stop         # Stop running container
make docker-clean        # Clean up Docker artifacts
```
