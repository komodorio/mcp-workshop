FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and kubectl
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg \
    && echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y kubectl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Create app directory
WORKDIR /app

# Copy dependency files and README (needed for build)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port for HTTP/SSE transport
EXPOSE 8000

# Set the working directory and activate venv in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default command (can be overridden)
CMD ["uv", "run", "mcp-server", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
