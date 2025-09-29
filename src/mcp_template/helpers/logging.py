"""Singleton MCP context logging utilities."""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession


class Logger:
    """Singleton logger that uses MCP context for sending messages to clients."""

    _instance: Optional["Logger"] = None
    _ctx: Optional[Context[ServerSession, Any]] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _auto_initialize(self, ctx: Optional[Context[ServerSession, Any]]) -> None:
        """Auto-initialize logger with context if not already initialized."""
        if ctx and self._ctx is None:
            self._ctx = ctx

    def _ensure_initialized(self) -> None:
        """Ensure logger is initialized, raise error if not."""
        if self._ctx is None:
            raise RuntimeError("Logger not initialized. No context available.")

    async def debug(
        self,
        message: str,
        component: str = "server",
        extra: Optional[Dict[str, Any]] = None,
        ctx: Optional[Context[ServerSession, Any]] = None,
    ) -> None:
        """Send debug message to client."""
        try:
            self._auto_initialize(ctx)
            self._ensure_initialized()
            formatted_message = f"[{component}] {message}"
            if extra:
                formatted_message += f" | {extra}"
            await self._ctx.debug(formatted_message)
        except (RuntimeError, ValueError):
            # Logger not initialized or context not available (tests) - ignore
            pass

    async def info(
        self,
        message: str,
        component: str = "server",
        extra: Optional[Dict[str, Any]] = None,
        ctx: Optional[Context[ServerSession, Any]] = None,
    ) -> None:
        """Send info message to client."""
        try:
            self._auto_initialize(ctx)
            self._ensure_initialized()
            formatted_message = f"[{component}] {message}"
            if extra:
                formatted_message += f" | {extra}"
            await self._ctx.info(formatted_message)
        except (RuntimeError, ValueError):
            # Logger not initialized or context not available (tests) - ignore
            pass

    async def warning(
        self,
        message: str,
        component: str = "server",
        extra: Optional[Dict[str, Any]] = None,
        ctx: Optional[Context[ServerSession, Any]] = None,
    ) -> None:
        """Send warning message to client."""
        try:
            self._auto_initialize(ctx)
            self._ensure_initialized()
            formatted_message = f"[{component}] {message}"
            if extra:
                formatted_message += f" | {extra}"
            await self._ctx.warning(formatted_message)
        except (RuntimeError, ValueError):
            # Logger not initialized or context not available (tests) - ignore
            pass

    async def error(
        self,
        message: str,
        component: str = "server",
        extra: Optional[Dict[str, Any]] = None,
        ctx: Optional[Context[ServerSession, Any]] = None,
    ) -> None:
        """Send error message to client."""
        try:
            self._auto_initialize(ctx)
            self._ensure_initialized()
            formatted_message = f"[{component}] {message}"
            if extra:
                formatted_message += f" | {extra}"
            await self._ctx.error(formatted_message)
        except (RuntimeError, ValueError):
            # Logger not initialized or context not available (tests) - ignore
            pass


# Global singleton instance
logger = Logger()
