.PHONY: help install test lint format run clean dev-setup

help: ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Dependencies installed"

test: ## Run all tests
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v

lint: ## Run linting
	@echo "🔍 Running linters..."
	uv run ruff check src/ tests/
	uv run mypy src/

format: ## Format code
	@echo "🎨 Formatting code..."
	uv run black src/ tests/
	uv run ruff check src/ tests/ --fix

run: ## Run the server in stdio mode
	@echo "🚀 Starting MCP server (stdio)..."
	uv run mcp-server

inspector: ## Run the server in stdio mode
	@echo "🚀 Starting MCP server (stdio)..."
	npx @modelcontextprotocol/inspector uv run mcp-server	

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

dev-setup: install ## Setup development environment
	@echo "🛠️  Setting up development environment..."
	uv run pre-commit install || true
	@echo "✅ Development environment ready!"
