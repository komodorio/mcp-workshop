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
   - Supports auto-reload for development

2. **SSE Transport** 
   - Server-Sent Events for real-time communication
   - Ideal for streaming applications
   - Port: 8000 (configurable)
   - Supports auto-reload for development

3. **STDIO Transport**
   - Standard input/output communication
   - Best for direct process communication
   - No network port required
   - Auto-reload not supported (process-based communication)

### Development Mode

For development, you can enable auto-reload which automatically restarts the server when source files change:

```bash
# HTTP with auto-reload
uv run mcp-server --transport http --reload

# SSE with auto-reload  
uv run mcp-server --transport sse --reload

# Using make command
make run-dev
```

**Auto-reload features:**
- Watches the `src/` directory for changes
- Automatically restarts the server on file modifications
- Only available for HTTP and SSE transports
- Ideal for rapid development and testing

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

## 🤖 Intelligent Prompts

The MCP server includes powerful prompt templates that help users leverage the Kubernetes tools more effectively. These prompts combine the kubectl functionality with AI agent capabilities for comprehensive cluster management.

### Available Prompts

#### 1. **diagnose_cluster_issues**
Advanced diagnostic prompt for comprehensive Kubernetes cluster troubleshooting.

**Parameters:**
- `context` (optional): Kubernetes context to diagnose. If not specified, uses the current context from kubectl config
- `namespace` (optional): Specific namespace to focus on. If not specified, checks all namespaces
- `focus_area` (default: "general"): Area to focus diagnostics on
  - `general`: Overall cluster health including nodes, pods, and system components
  - `pods`: Pod status, restarts, resource usage, and container issues  
  - `services`: Service endpoints, load balancers, and networking configuration
  - `networking`: Network policies, DNS resolution, and connectivity issues
  - `storage`: Persistent volumes, storage classes, and mount issues
  - `performance`: Resource utilization, bottlenecks, and scaling issues

**Features:**
- Systematic cluster analysis with structured diagnostic workflow
- Prioritized issue identification with remediation steps
- Visual summary with Mermaid diagrams showing issue locations
- Color-coded status indicators (🟢 healthy, 🟡 warning, 🔴 critical)

#### 2. **cluster_health_overview**
Comprehensive cluster health overview with monitoring dashboard capabilities.

**Parameters:**
- `context` (optional): Kubernetes context to analyze. If not specified, uses the current context from kubectl config
- `include_metrics` (default: true): Include detailed resource metrics and utilization
- `generate_dashboard` (default: false): Generate visual dashboard representation

**Features:**
- Executive summary with overall health score (0-100)
- Infrastructure status including nodes, control plane, and networking
- Workload health summary with deployment status analysis
- Security & compliance review (RBAC, network policies, pod security)
- Resource metrics and capacity planning recommendations
- Visual dashboard with Mermaid architecture diagrams

#### 3. **troubleshoot_workload**
Targeted troubleshooting for specific Kubernetes workloads.

**Parameters:**
- `workload_type`: Type of workload (deployment, pod, service, statefulset, etc.)
- `workload_name`: Name of the specific workload to troubleshoot
- `namespace` (default: "default"): Namespace where the workload is located
- `context` (optional): Kubernetes context to use. If not specified, uses the current context from kubectl config
- `include_logs` (default: true): Include log analysis in troubleshooting

**Features:**
- Systematic troubleshooting workflow with 8-step analysis
- Root cause analysis with dependency mapping
- Configuration validation and network connectivity testing
- Event timeline analysis and log pattern recognition
- Remediation plan with specific kubectl commands and rollback procedures

#### 4. **generate_architecture_diagram**
Create comprehensive Kubernetes architecture diagrams with multiple scope options.

**Parameters:**
- `scope` (default: "cluster"): Scope of diagram
  - `cluster`: High-level cluster architecture with nodes and namespaces
  - `namespace`: Detailed namespace architecture with workload relationships
  - `application`: Application-level microservices and data flow
  - `networking`: Network topology, ingress, and communication patterns
- `context` (optional): Kubernetes context to diagram. If not specified, uses the current context from kubectl config
- `namespace` (optional): Specific namespace for namespace/application scope
- `include_networking` (default: true): Include detailed networking components
- `diagram_format` (default: "mermaid"): Format for diagram (mermaid, plantuml, ascii)

**Features:**
- Multi-scope architecture visualization from cluster to application level
- Infrastructure, workload, and security boundary mapping
- Data flow and dependency visualization with clear hierarchy
- Color coding and legend for different component types
- Integration with monitoring and logging flows

### Usage Examples

**Basic cluster diagnosis:**
```python
# Diagnose general cluster issues
prompt = diagnose_cluster_issues()

# Focus on pod-specific issues in production context
prompt = diagnose_cluster_issues(context="production", focus_area="pods")

# Diagnose networking issues in specific namespace
prompt = diagnose_cluster_issues(context="staging", namespace="app-namespace", focus_area="networking")
```

**Health overview with dashboard:**
```python
# Basic health overview
prompt = cluster_health_overview()

# Full health report with metrics and visual dashboard
prompt = cluster_health_overview(context="production", include_metrics=True, generate_dashboard=True)
```

**Workload troubleshooting:**
```python
# Troubleshoot a failing deployment
prompt = troubleshoot_workload("deployment", "web-app", namespace="production")

# Troubleshoot pod without log analysis
prompt = troubleshoot_workload("pod", "db-pod-123", namespace="database", include_logs=False)
```

**Architecture diagrams:**
```python
# Cluster-wide architecture diagram
prompt = generate_architecture_diagram(scope="cluster", context="production")

# Application-specific diagram with networking focus
prompt = generate_architecture_diagram(
    scope="application", 
    namespace="microservices", 
    include_networking=True,
    diagram_format="mermaid"
)
```

### Integration with AI Agents

These prompts are designed to work seamlessly with AI agents and provide:

1. **Structured Workflows**: Each prompt follows a systematic approach that guides the AI through comprehensive analysis
2. **Visual Artifacts**: Integration with Mermaid diagrams for creating visual dashboards and architecture representations
3. **Actionable Outputs**: Prompts generate specific kubectl commands and remediation steps
4. **Context Awareness**: Smart parameter handling for different environments and scopes
5. **Extensible Design**: Easy to customize and extend for specific organizational needs

### Best Practices

- **Start with Overview**: Use `cluster_health_overview` for general assessment before diving into specific issues
- **Focus Your Diagnosis**: Use appropriate `focus_area` parameters to target specific problem domains  
- **Combine Prompts**: Use multiple prompts together for comprehensive analysis (e.g., overview + specific troubleshooting)
- **Leverage Visuals**: Enable dashboard generation for stakeholder communication and documentation
- **Context Specificity**: Always specify the appropriate context and namespace for accurate results

---

## 🛠️ Available Tools

The MCP server provides the following tools for interacting with Kubernetes clusters:

### kubectl

Execute kubectl commands with comprehensive error handling and safety features.

**Parameters:**
- `cmd`: kubectl command as a string (without 'kubectl' prefix) - **required**
- `context` (optional): Kubernetes context to use. If not specified, uses the current context from kubectl config
- `namespace` (optional): Kubernetes namespace to use. If not specified, uses "default"
- `output_format` (default: "json"): Output format (json, yaml, table, etc.)
- `timeout` (default: 30.0): Command timeout in seconds

**Safety Features:**
- Automatic confirmation prompt for dangerous commands (delete, apply, create, patch, etc.)
- Comprehensive error handling with detailed error messages
- JSON parsing support for structured output
- Context-aware execution with MCP logging integration

**Usage Examples:**
```python
# Get all pods using current context and default namespace
kubectl("get pods")

# Get pods in specific namespace
kubectl("get pods", namespace="kube-system", output_format="table")

# Describe pod in specific context
kubectl("describe pod my-pod", context="production")

# Get logs with tail
kubectl("logs deployment/my-app --tail=100")

# Dangerous operation (will prompt for confirmation)
kubectl("delete pod my-pod")
```

### base64

Encode or decode base64 text for working with Kubernetes secrets and configurations.

**Parameters:**
- `text`: The text to encode or base64 string to decode - **required**
- `action`: Action to perform - "encode" or "decode" - **required**
- `encoding` (default: "utf-8"): Text encoding to use

**Usage Examples:**
```python
# Encode text to base64
base64("Hello World", "encode")
# Returns: "SGVsbG8gV29ybGQ="

# Decode base64 string
base64("SGVsbG8gV29ybGQ=", "decode")
# Returns: "Hello World"

# Encode with specific encoding
base64("Hello 世界", "encode", "utf-8")
# Returns: "SGVsbG8g5LiW55WM"
```

### Default Behavior

**Context Parameter:**
- When `context` is not specified (or set to `None`), the tools will automatically use the current context from your kubectl config
- This means you can start using the tools immediately without specifying a context
- To check your current context: `kubectl config current-context`

**Namespace Parameter:**
- When `namespace` is not specified, it defaults to "default"
- For prompts that support namespace=None, all namespaces will be checked

---

## 🚀 Kubernetes Deployment + OpenTelemetry Monitoring

This MCP server includes production-ready Kubernetes manifests with comprehensive monitoring and observability.

### Prerequisites

- Kubernetes cluster with nginx ingress controller
- Container image pushed to a registry (e.g., `ghcr.io/your-org/mcp-server:latest`)
- TLS certificate secret (optional, for HTTPS)

### Quick Start

1. **Update image and domain in manifests:**
```bash
# Update the image in k8s/deployment.yaml
sed -i 's|ghcr.io/your-org/mcp-server:latest|your-registry/mcp-server:latest|g' k8s/deployment.yaml

# Update domain in k8s/ingress.yaml
sed -i 's|mcp.YOUR_DOMAIN|mcp.example.com|g' k8s/ingress.yaml
```

2. **Deploy to Kubernetes:**
```bash
# Apply all manifests
kubectl apply -f infra/

# Or use kustomize
kubectl apply -k infra/
```

3. **Verify deployment:**
```bash
# Check pods
kubectl get pods -n mcp

# Check service
kubectl get svc -n mcp

# Test health endpoint
kubectl port-forward -n mcp svc/mcp-server 8080:80
curl http://localhost:8080/mcp
```

### OpenTelemetry Integration

#### Adding Telemetry to Your Tools

Use the `@tracer()` decorator to instrument your MCP tools:

```python
from mcp_template.telemetry import tracer
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="my-mcp-server")

@mcp.tool()
@tracer(
    name="tool.run_kubectl",
    redact_keys={"token", "secret", "password"},
    arg_denylist={"ctx"},
)
async def run_kubectl(cmd: str, context: str = None, ctx: Context = None) -> str:
    """Run kubectl command with telemetry."""
    # Your tool implementation
    return "command output"
```

#### Enabling Telemetry Export

By default, telemetry exporters are disabled to prevent failures when no collector is available. To enable:

```bash
# Enable OTLP export to collector
kubectl -n mcp set env deploy/mcp-server \
  OTEL_TRACES_EXPORTER=otlp \
  OTEL_METRICS_EXPORTER=otlp \
  OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.mcp.svc.cluster.local:4317 \
  OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
  OTEL_EXPORTER_OTLP_TIMEOUT=2000
```

### Monitoring Components

#### 1. OpenTelemetry Collector

- **Purpose**: Receives traces/metrics from MCP server, exports to monitoring backends
- **Endpoints**: 
  - OTLP gRPC: `otel-collector.mcp.svc.cluster.local:4317`
  - OTLP HTTP: `otel-collector.mcp.svc.cluster.local:4318`
- **Configuration**: Modify `infra/otel-collector.yaml` ConfigMap to add exporters

#### 2. Prometheus Monitoring

- ServiceMonitor included for Prometheus operator
- Metrics exposed on `/metrics` endpoint
- Collector metrics available on port 8888

#### 3. Health Checks

- **Root**: `/mcp` - service information

### Scaling and Reliability

#### Horizontal Pod Autoscaler (HPA)
- Scales 2-6 replicas based on CPU (70%) and memory (80%)
- Custom scaling policies for smooth scaling behavior

#### Pod Disruption Budget (PDB)
- Ensures minimum 1 replica during cluster maintenance
- Protects against voluntary disruptions

#### Resource Management
- **Requests**: 250m CPU, 256Mi memory
- **Limits**: 1 CPU, 512Mi memory
- **Security**: Non-root user, read-only filesystem, dropped capabilities

### Customization

#### Environment Variables

Key environment variables in deployment:

```yaml
env:
  # OpenTelemetry
  - name: OTEL_SERVICE_NAME
    value: "mcp-server"
  - name: OTEL_TRACES_EXPORTER
    value: "none"  # Change to "otlp" to enable
  - name: OTEL_RESOURCE_ATTRIBUTES
    value: "service.namespace=mcp,deployment.environment=prod"
  
  # Add your custom variables
  - name: LOG_LEVEL
    value: "INFO"
```

#### Ingress Configuration

Customize ingress annotations in `infra/ingress.yaml`:

```yaml
annotations:
  # Timeouts for long-running operations
  nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
  nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
  
  # CORS for web clients
  nginx.ingress.kubernetes.io/enable-cors: "true"
  
  # Rate limiting (optional)
  nginx.ingress.kubernetes.io/rate-limit: "100"
```

### Production Checklist

- [ ] Update image registry and tag in `infra/deployment.yaml`
- [ ] Configure domain name in `infra/ingress.yaml`
- [ ] Create TLS certificate secret
- [ ] Review resource requests/limits
- [ ] Configure monitoring backend exporters
- [ ] Set up log aggregation
- [ ] Configure alerting rules
- [ ] Test rolling updates
- [ ] Verify backup/restore procedures
