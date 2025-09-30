"""Core MCP server implementation using FastMCP."""

from mcp.server.fastmcp import FastMCP

from . import prompts, resources, tools

# Initialize OpenTelemetry instrumentation
try:
    import os

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    # Only set up if not already configured
    if not isinstance(trace.get_tracer_provider(), TracerProvider):
        # Create resource with service information
        resource = Resource.create(
            {
                "service.name": os.getenv("OTEL_SERVICE_NAME", "mcp-server"),
                "service.version": "0.1.0",
            }
        )

        # Set up tracer provider
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)

        # Add OTLP exporter if enabled
        if os.getenv("OTEL_TRACES_EXPORTER", "none") == "otlp":
            otlp_exporter = OTLPSpanExporter(
                endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
                insecure=True,
            )
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)

except ImportError:
    # OpenTelemetry not available, continue without instrumentation
    pass


def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    # Create FastMCP server with lifespan management
    mcp = FastMCP(name="mcp-server", instructions="You are a Kubernetes operations assistant. Use kubectl tool to inspect pods, deployments, services, and logs. Use base64 tool to decode secrets or encode config data. Always check current cluster context first, request user confirmation for any destructive operations, and provide actionable troubleshooting steps.")

    # Register all handlers with the mcp instance
    prompts.register_prompts(mcp)
    tools.register_tools(mcp)
    resources.register_resources(mcp)

    return mcp
