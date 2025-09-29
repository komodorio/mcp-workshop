"""
Prompts implementation for MCP server.

This is where you define your prompts. Users mainly need to modify this file.
"""

from typing import Optional
from mcp.server.fastmcp import FastMCP, Context


def register_prompts(mcp: FastMCP) -> None:
    """Register all prompts with the FastMCP server."""

    @mcp.prompt()
    def diagnose_cluster_issues(
        context: Optional[str] = None, namespace: Optional[str] = None, focus_area: str = "general"
    ) -> str:
        """Generate a comprehensive diagnostic prompt for Kubernetes cluster issues.

        Args:
            context: Kubernetes context to diagnose (optional, uses current if not specified)
            namespace: Specific namespace to focus on (optional, checks all if not specified)
            focus_area: Area to focus diagnostics on - general, pods, services, networking, storage, or performance
        """
        context_info = f" in context '{context}'" if context else ""
        namespace_info = f" in namespace '{namespace}'" if namespace else " across all namespaces"

        diagnostic_areas = {
            "general": "overall cluster health including nodes, pods, and system components",
            "pods": "pod status, restarts, resource usage, and container issues",
            "services": "service endpoints, load balancers, and networking configuration",
            "networking": "network policies, DNS resolution, and connectivity issues",
            "storage": "persistent volumes, storage classes, and mount issues",
            "performance": "resource utilization, bottlenecks, and scaling issues",
        }

        focus_description = diagnostic_areas.get(focus_area, "general cluster health")

        return f"""Please perform a comprehensive Kubernetes cluster diagnostic focused on {focus_description}{context_info}{namespace_info}.

Use the available kubectl tools to:

1. **Cluster Overview**:
   - Check cluster info and node status
   - Identify any nodes with issues (NotReady, MemoryPressure, DiskPressure)
   - Review system pods in kube-system namespace

2. **Resource Analysis**:
   - List pods with non-Running status (Pending, CrashLoopBackOff, Error)
   - Check for pods with high restart counts
   - Identify resource-constrained pods

3. **Event Investigation**:
   - Examine recent cluster events for warnings or errors
   - Focus on events related to the {focus_area} area

4. **Generate Summary**:
   - Create a prioritized list of issues found
   - Provide specific remediation steps for each issue
   - Include relevant kubectl commands for further investigation

5. **Visual Summary** (if needed):
   - Create a Mermaid diagram showing the cluster topology and issue locations
   - Use color coding: 🟢 healthy, 🟡 warning, 🔴 critical

Please start by gathering the cluster information and then provide a structured diagnostic report."""

    @mcp.prompt()
    def cluster_health_overview(
        context: Optional[str] = None,
        include_metrics: bool = True,
        generate_dashboard: bool = False,
    ) -> str:
        """Generate a prompt for comprehensive cluster health overview and monitoring dashboard.

        Args:
            context: Kubernetes context to analyze (optional, uses current if not specified)
            include_metrics: Whether to include detailed resource metrics and utilization
            generate_dashboard: Whether to generate a visual dashboard representation
        """
        context_info = f" for context '{context}'" if context else ""

        dashboard_section = (
            """
6. **Visual Dashboard** (create a comprehensive monitoring dashboard):
   - Generate a Mermaid diagram showing cluster architecture
   - Create charts showing resource utilization trends
   - Include status indicators for all major components
   - Add capacity planning recommendations
"""
            if generate_dashboard
            else ""
        )

        metrics_section = (
            """
4. **Resource Metrics & Utilization**:
   - CPU and memory usage across nodes and pods
   - Storage utilization and available capacity
   - Network traffic patterns and bottlenecks
   - Identify over/under-provisioned resources

5. **Capacity Planning**:
   - Current vs. requested vs. allocated resources
   - Scaling recommendations for deployments
   - Node capacity analysis and expansion needs
"""
            if include_metrics
            else ""
        )

        return f"""Please provide a comprehensive Kubernetes cluster health overview{context_info}.

Analyze and report on:

1. **Cluster Infrastructure Status**:
   - Node health, versions, and capacity
   - Control plane components status
   - etcd health and backup status
   - Network plugin and DNS functionality

2. **Workload Health Summary**:
   - Application deployments and their status
   - Pod distribution and scheduling efficiency
   - Service mesh health (if applicable)
   - Ingress controllers and load balancers

3. **Security & Compliance**:
   - RBAC configuration review
   - Network policies effectiveness
   - Pod security standards compliance
   - Secret and ConfigMap usage patterns
{metrics_section}{dashboard_section}
Format the output as a structured health report with:
- Executive summary with overall health score (0-100)
- Color-coded status indicators (🟢🟡🔴)
- Immediate action items prioritized by severity
- Trending analysis showing improvement/degradation over time

Start by gathering cluster information using the available kubectl tools."""

    @mcp.prompt()
    def troubleshoot_workload(
        workload_type: str,
        workload_name: str,
        namespace: str = "default",
        context: Optional[str] = None,
        include_logs: bool = True,
    ) -> str:
        """Generate a targeted troubleshooting prompt for specific Kubernetes workloads.

        Args:
            workload_type: Type of workload (deployment, pod, service, statefulset, etc.)
            workload_name: Name of the specific workload to troubleshoot
            namespace: Namespace where the workload is located
            context: Kubernetes context to use
            include_logs: Whether to include log analysis in troubleshooting
        """
        context_info = f" in context '{context}'" if context else ""
        log_section = (
            """
6. **Log Analysis**:
   - Retrieve and analyze recent logs from all containers
   - Look for error patterns, stack traces, and warning messages
   - Check for resource exhaustion indicators
   - Examine startup and shutdown sequences
"""
            if include_logs
            else ""
        )

        return f"""Please troubleshoot the {workload_type} '{workload_name}' in namespace '{namespace}'{context_info}.

Perform systematic troubleshooting:

1. **Current Status Assessment**:
   - Get detailed status of the {workload_type}
   - Check replicas, ready state, and conditions
   - Identify any status anomalies or error conditions

2. **Resource Investigation**:
   - Examine resource requests and limits
   - Check for resource constraints (CPU, memory, storage)
   - Verify node scheduling and affinity rules

3. **Configuration Validation**:
   - Review environment variables and ConfigMaps
   - Validate mounted secrets and volumes
   - Check service account and RBAC permissions

4. **Network Connectivity**:
   - Test service endpoints and port connectivity
   - Validate ingress rules and load balancer configuration
   - Check network policies affecting the workload

5. **Event Timeline**:
   - Examine recent events related to the workload
   - Identify patterns in failures or restarts
   - Check for scheduling or resource allocation issues
{log_section}
7. **Dependency Analysis**:
   - Check health of dependent services and databases
   - Validate external connectivity and DNS resolution
   - Review service mesh configuration (if applicable)

8. **Remediation Plan**:
   - Provide step-by-step troubleshooting actions
   - Include specific kubectl commands for fixes
   - Create rollback plan if needed

Please create a detailed troubleshooting report with root cause analysis and actionable solutions."""

    @mcp.prompt()
    def generate_architecture_diagram(
        scope: str = "cluster",
        context: Optional[str] = None,
        namespace: Optional[str] = None,
        include_networking: bool = True,
        diagram_format: str = "mermaid",
    ) -> str:
        """Generate a prompt to create comprehensive Kubernetes architecture diagrams.

        Args:
            scope: Scope of diagram (cluster, namespace, application, networking)
            context: Kubernetes context to diagram
            namespace: Specific namespace to focus on (for namespace/application scope)
            include_networking: Whether to include detailed networking components
            diagram_format: Format for diagram (mermaid, plantuml, ascii)
        """
        context_info = f" in context '{context}'" if context else ""
        namespace_info = f" focusing on namespace '{namespace}'" if namespace else ""

        scope_instructions = {
            "cluster": "Create a high-level cluster architecture showing nodes, namespaces, and major components",
            "namespace": f"Detail the architecture within namespace '{namespace}' showing all workloads and their relationships",
            "application": f"Focus on application-level architecture within '{namespace}' showing microservices and data flow",
            "networking": "Emphasize network topology, ingress, services, and communication patterns",
        }

        instruction = scope_instructions.get(scope, scope_instructions["cluster"])

        network_section = (
            """
- Network policies and traffic flow
- Ingress controllers and load balancers  
- Service mesh components (if present)
- DNS and service discovery patterns
"""
            if include_networking
            else ""
        )

        return f"""Please create a comprehensive Kubernetes architecture diagram{context_info}{namespace_info}.

{instruction}

Gather information and create a {diagram_format} diagram including:

**Infrastructure Components:**
- Nodes (control plane and worker nodes)
- Storage classes and persistent volumes
- Network infrastructure and CNI details
{network_section}
**Application Workloads:**
- Deployments, StatefulSets, DaemonSets
- Pods and their container relationships
- Services and their endpoint mappings
- ConfigMaps and Secrets usage

**Data Flow & Dependencies:**
- Inter-service communication patterns
- External system integrations
- Database connections and data persistence
- Monitoring and logging flows

**Security Boundaries:**
- RBAC roles and service accounts
- Network segmentation and policies
- Secret management and access patterns

Create the diagram with:
1. Clear visual hierarchy and grouping
2. Color coding for different component types
3. Arrows showing data/traffic flow
4. Labels indicating resource types and statuses
5. Legend explaining symbols and color meanings

Use the kubectl tools to gather all necessary information, then generate a well-structured {diagram_format} diagram that accurately represents the current architecture."""
