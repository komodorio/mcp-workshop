# MCP Kubernetes Server Workshop
## From Blueprint to Production: Building Intelligent Kubernetes Management

> **🎯 This workshop teaches you to build advanced [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/python-sdk) servers for production-ready AI-tool integrations. You'll learn sophisticated patterns including interactive elicitation, multi-transport support, structured resources, and expert-level prompt engineering through hands-on Kubernetes management.**

---

## 🎯 What is MCP (Model Context Protocol)?

**Model Context Protocol (MCP)** is a revolutionary standardized protocol that enables AI assistants to securely interact with external systems, tools, and data sources. Think of it as the "API for AI" - a bridge that allows language models like Claude, ChatGPT, and others to go beyond text generation and actually perform real-world actions.

**In this workshop, you'll go beyond basic MCP usage**, learning advanced patterns from the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) including elicitation, multi-transport architecture, structured logging, and production-ready safety mechanisms.

### Why MCP Matters

**Traditional AI Limitations:**
- AI assistants are isolated from external systems
- No standardized way to interact with tools and data
- Each integration requires custom implementation
- Limited to text-based responses only

**MCP Solution:**
- **Standardized Protocol** - One protocol for all AI-tool integrations
- **Secure Communication** - Built-in security and permission management  
- **Bidirectional Flow** - AI can both query data and perform actions
- **Extensible Architecture** - Easy to add new capabilities and integrations

### Why Use MCP for Kubernetes?

❌ **Without MCP:** "Please run `kubectl get pods -n production` and paste the output"  
✅ **With MCP:** "Show me all failing pods in production and suggest fixes"

**Key Benefits:**
- **Natural Language Operations** - Manage clusters through conversation
- **Intelligent Troubleshooting** - AI-powered problem diagnosis
- **Automated Workflows** - Chain multiple operations intelligently  
- **Context-Aware Actions** - AI understands your cluster state
- **Reduced Cognitive Load** - No more memorizing kubectl commands

---

## 🏗️ The Three Pillars of MCP

### 1. 🛠️ **Tools**
Tools are the **actions** your AI assistant can perform. They define what the AI can do.

**Examples:**
- `kubectl_execute` - Run any kubectl command
- `troubleshoot_pod` - Diagnose pod issues
- `scale_deployment` - Adjust replica counts
- `get_cluster_health` - Assess overall cluster status

**Tool Characteristics:**
- **Input Parameters** - What data the tool needs
- **Output Format** - Structured response for AI consumption
- **Error Handling** - Graceful failure management
- **Documentation** - Clear descriptions for AI understanding

### 2. 📚 **Resources**
Resources are the **data sources** your AI assistant can access. They provide context and information.

**Examples:**
- Cluster configuration and state
- Pod logs and events  
- Deployment histories
- Resource metrics and quotas
- Network policies and services

**Resource Types:**
- **Static Resources** - Configuration files, documentation
- **Dynamic Resources** - Real-time cluster state, metrics
- **Computed Resources** - Analyzed data, health scores
- **External Resources** - Monitoring systems, registries

### 3. 💬 **Prompts** 
Prompts are the **interaction patterns** that define how humans communicate with the AI assistant.

**Categories:**
- **Diagnostic Prompts** - "Why is my app crashing?"
- **Operational Prompts** - "Scale my web service to handle more traffic"
- **Exploratory Prompts** - "Show me the health of my cluster"
- **Complex Workflow Prompts** - "Deploy this configuration and monitor the rollout"

**Prompt Design Principles:**
- **Natural Language** - Conversational, not command-line syntax
- **Context-Aware** - AI understands your cluster state
- **Action-Oriented** - Focus on outcomes, not technical details
- **Error-Resilient** - Handle ambiguity gracefully

---

## 🎯 What We're Building

### **Project: Intelligent Kubernetes MCP Server**

We're building a production-ready MCP server that transforms Kubernetes management from command-line complexity to natural language conversation.

**Core Capability:**
```
Human: "My payment service is acting up, what's wrong with it?"

AI: "I found your payment-service pod is in CrashLoopBackOff state. 
    Looking at the logs, it's failing to connect to the database. 
    The error suggests the DB_HOST environment variable is incorrect.
    
    Would you like me to:
    1. Show you the current environment variables
    2. Check if the database service is running
    3. Help you update the configuration?"
```

### **Why This Approach?**

**🔧 Single Powerful Tool Strategy:**
- One `kubectl_execute` tool that can run any kubectl command
- Maximum flexibility with minimal complexity
- Easy to understand and extend
- Covers 100% of Kubernetes operations

**🧠 AI-Powered Intelligence:**
- AI translates natural language to appropriate kubectl commands
- Interprets results and provides insights
- Chains multiple commands for complex workflows
- Provides contextual recommendations

**🏗️ Production-Ready Architecture:**
- Error handling and validation
- Security and permission management
- Monitoring and observability
- Scalable deployment patterns

---

## 🌿 Workshop Structure: Branch-Based Learning

We'll use git branches to organize our learning journey, with each branch representing a complete milestone.

### **Branch: `start`** 
**Goal:** Foundation and environment preparation
- MCP framework installation
- Kubernetes cluster access
- Development environment setup
- Basic server scaffolding

**Deliverables:**
- Working development environment
- Basic MCP server template
- Kubernetes connectivity verified

---

### **Branch: `resources`**
**Goal:** Define and implement data sources
- kubectl contexts
- k8s info
- k8s namespaces

**Deliverables:**
- Resource discovery mechanisms
- Data access patterns
- Caching and performance optimization

---

### **Branch: `tools`**
**Goal:** Implement the core kubectl execution tool
- `kubectl_execute` tool implementation
- Command validation and security
- Output parsing and formatting
- Error handling and user feedback

**Deliverables:**
- Production-ready kubectl tool
- Comprehensive error handling
- Security validations
- Output formatting

---

### **Branch: `prompts`**
**Goal:** Design interaction patterns and examples
- Natural language prompt templates
- Use case scenarios and examples
- Conversational workflow patterns
- Documentation and guides

**Deliverables:**
- 50+ example prompts
- Interaction pattern library
- User experience guidelines
- Demo scenarios

---

### **Branch: `deploy-monitor`**
**Goal:** Production deployment and observability
- Containerization and orchestration
- Health checks and monitoring
- Performance optimization
- Scaling patterns

**Deliverables:**
- Production deployment manifests
- Monitoring and alerting setup
- Performance benchmarks
- Operational runbooks

---

### **Branch: `komodor-mcp`** 
**Goal:** Advanced integration with Komodor platform
- Komodor API integration
- Enhanced troubleshooting capabilities
- Advanced monitoring and insights
- Production-grade observability

**Deliverables:**
- Komodor MCP integration
- Advanced diagnostic capabilities
- Production monitoring dashboards

---

**Advanced MCP Capabilities:**
- **Interactive Elicitation** - User confirmations for dangerous operations
- **Multi-Transport Support** - stdio, SSE, and HTTP transports  
- **Structured Logging** - Component-based observability
- **Type-Safe Resources** - Pydantic models for validation
- **Error Handling** - Custom exceptions and graceful degradation
- **Context-Aware Execution** - Automatic kubectl context resolution
- **50+ Expert Prompts** - Diagnostic and operational templates

---

## 🚀 **Quick Start: Setup & Configuration**

### **Prerequisites**
- Python 3.10+ installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- kubectl installed and configured
- Access to a Kubernetes cluster

### **1. Clone and Install**

```bash
# Clone the workshop repository
git clone https://github.com/komodorio/mcp-workshop
cd mcp-workshop

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using Makefile
make install

# Setup development environment (optional)
make dev-setup

# Verify installation
uv run mcp-server --help
```

### **2. Development Workflow**

The project includes a comprehensive Makefile with common development tasks:

```bash
# See all available commands
make help

# Run the server (different modes)
make run              # stdio mode (for AI assistants)
make run-http         # HTTP mode
make run-dev          # HTTP with auto-reload for development

# Development tools
make test             # Run tests
make lint             # Run linting
make format           # Format code
make clean            # Clean build artifacts

# MCP Inspector (debug tool)
make inspector        # Run with MCP inspector for debugging
```

### **3. Test the Server**

```bash
# Quick test with stdio transport
make run

# Development server with auto-reload
make run-dev

# Manual command examples
uv run mcp-server --transport stdio
uv run mcp-server --transport http --host localhost --port 8000
uv run mcp-server --transport http --reload  # auto-reload for development
```

### **4. Debug with VS Code**

The project includes VS Code launch configurations for debugging:

- **Debug MCP Server (stdio)** - For testing with AI clients
- **Debug MCP Server (HTTP)** - For web-based testing  
- **Debug MCP Server (HTTP + Auto-reload)** - For development

Press `F5` in VS Code and select your preferred configuration.

### **3. Configure with Cursor**

Add to your Cursor MCP settings (`.cursor/mcp_servers.json`):

```json
{
  "mcp-k8s-server": {
    "command": "uv",
    "args": [
      "run", 
      "mcp-server", 
      "--transport", 
      "stdio"
    ],
    "cwd": "/path/to/mcp-workshop",
    "env": {
      "KUBECONFIG": "/path/to/your/kubeconfig"
    }
  }
}
```

### **4. Configure with Claude Desktop**

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "mcp-k8s-server": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/mcp-workshop",
      "env": {
        "KUBECONFIG": "/path/to/your/kubeconfig"
      }
    }
  }
}
```

### **5. Verify Connection**

Once configured, you should see:
- **Available Tools**: `kubectl` - Execute Kubernetes commands
- **Available Resources**: Context discovery, cluster info, namespaces
- **Available Prompts**: Diagnostic workflows, architecture diagrams

### **6. Example Usage**

Try these commands in your AI assistant:

```
"Show me all pods in the default namespace"
"Diagnose issues in my production cluster"  
"Create an architecture diagram of my cluster"
"Scale my web deployment to 3 replicas"
```

The server will automatically handle safety confirmations for dangerous operations and provide structured, actionable responses.

### **7. Advanced Development & Deployment**

#### **MCP Inspector (Debugging)**
Use the official MCP Inspector for debugging and testing:

```bash
# Run server with MCP Inspector
make inspector

# Manual command
npx @modelcontextprotocol/inspector uv run mcp-server
```

The inspector provides a web interface to test tools, resources, and prompts interactively.

#### **Docker Deployment**
For containerized deployment:

```bash
# Build and run with Docker
make docker-build      # Build Docker image
make docker-run        # Run container with HTTP transport on port 8000

# Cleanup
make docker-stop       # Stop running container
make docker-clean      # Remove containers and images
```

#### **Development Best Practices**

```bash
# Complete development workflow
make dev-setup         # Setup pre-commit hooks and dev tools
make format           # Format code before committing
make lint             # Check code quality
make test             # Run test suite
make run-dev          # Start development server with auto-reload
```

---

## 🎪 Workshop Experience

### **What You'll Build**
- **Intelligent Kubernetes Assistant** - Chat with your clusters in natural language
- **Powerful Troubleshooting Tool** - AI-powered problem diagnosis
- **Production-Ready Solution** - Deploy to your own infrastructure
- **Extensible Framework** - Foundation for building more tools

### **What You'll Learn**
- **MCP Protocol Fundamentals** - How AI-tool integration works
- **Kubernetes API Mastery** - Programmatic cluster management
- **AI-Assisted Operations** - The future of infrastructure management
- **Production Deployment** - Take your tools to production

### **What You'll Take Away**
- **Working MCP Server** - Immediately usable in your environment
- **Complete Source Code** - Well-documented, production-ready
- **Deployment Templates** - Docker, Kubernetes, monitoring setup
- **Extensibility Guide** - How to add your own tools and integrations

---

## 🚀 Ready to Transform Kubernetes Management?

This project showcases how **advanced MCP capabilities** can transform complex infrastructure management into intelligent, conversational operations. You'll learn patterns that bridge command-line complexity with natural language interaction, all while maintaining enterprise-grade safety and reliability.

**The future of AI-powered infrastructure management is here - let's build it together!**