# MCP Server Kubernetes Deployment

Simple, practical Kubernetes deployment for the MCP server.

## Quick Deploy

1. **Update the image**:
   ```bash
   # Edit infra/deployment.yaml and replace:
   # ghcr.io/your-org/mcp-server:latest
   # with your actual image
   ```

2. **Deploy**:
   ```bash
   kubectl apply -f infra/
   ```

3. **Check it's running**:
   ```bash
   kubectl get pods -n mcp
   kubectl port-forward -n mcp svc/mcp-server 8080:80
   curl http://localhost:8080/healthz
   ```

## What's Included

- **Namespace**: `mcp` namespace for isolation
- **Deployment**: 2 replicas with health checks
- **Service**: ClusterIP service on port 80

## Resource Usage

- **CPU**: 100m request, 500m limit
- **Memory**: 128Mi request, 256Mi limit
- **Storage**: None (stateless)

## Monitoring

OpenTelemetry is included but **disabled by default**. To enable:

```bash
# Enable telemetry export
kubectl -n mcp set env deploy/mcp-server \
  OTEL_TRACES_EXPORTER=otlp \
  OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317
```

## Scaling

```bash
# Scale up/down manually
kubectl -n mcp scale deploy/mcp-server --replicas=3
```

## Troubleshooting

```bash
# Check pod status
kubectl get pods -n mcp

# Check logs
kubectl logs -n mcp -l app=mcp-server

# Check service
kubectl get svc -n mcp

# Test locally
kubectl port-forward -n mcp svc/mcp-server 8080:80
```

That's it! No over-engineering, just the basics that work.
