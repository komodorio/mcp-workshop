"""OpenTelemetry tracer decorator for MCP tools."""

import asyncio
import inspect
import re
from collections.abc import Callable, Iterable
from functools import wraps
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.trace.status import Status, StatusCode

TracerLike = trace.Tracer

SECRET_VALUE_RE = re.compile(
    r"(?:^|[^a-zA-Z])(token|secret|password|apikey|api_key|bearer)[^a-zA-Z]?", re.I
)


def _truncate(value: Any, max_len: int = 256) -> str:
    try:
        s = str(value)
    except Exception:
        s = repr(value)
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def _should_redact(key: str, value: Any, redact_keys: Iterable[str]) -> bool:
    if key.lower() in {k.lower() for k in redact_keys}:
        return True
    if any(
        x in key.lower()
        for x in ["token", "secret", "password", "passwd", "apikey", "api_key", "bearer"]
    ):
        return True
    if isinstance(value, str) and SECRET_VALUE_RE.search(value or ""):
        return True
    return False


def _bind_args(func: Callable, args: tuple, kwargs: dict) -> dict[str, Any]:
    sig = inspect.signature(func)
    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)


def tracer(
    name: str | None = None,
    *,
    attribute_prefix: str = "mcp.tool",
    arg_allowlist: Iterable[str] | None = None,
    arg_denylist: Iterable[str] | None = None,
    redact_keys: Iterable[str] = (),
    capture_return_len: bool = True,
    max_value_len: int = 256,
    kind: SpanKind = SpanKind.INTERNAL,
    tracer_provider: TracerLike | None = None,
) -> Callable[[Callable], Callable]:
    """
    Decorator factory for instrumenting MCP tool functions.

    Args:
      name: span name; defaults to f"tool.{func.__name__}"
      attribute_prefix: prefix for attributes (e.g., mcp.tool.arg.<key>)
      arg_allowlist: if provided, only these argument names are recorded
      arg_denylist: arguments to skip even if allowlisted
      redact_keys: arguments to record but as "***"
      capture_return_len: add <prefix>.return_length attribute (len(str(result)))
      max_value_len: truncate attribute values to this length
      kind: SpanKind, default INTERNAL
      tracer_provider: optional custom tracer (else global)

    Usage:
      @mcp.tool()
      @tracer()
      async def run_cmd(cmd: str) -> str:
          ...
    """
    _tracer = tracer_provider or trace.get_tracer("mcp.fastmcp.tools")

    def decorator(func: Callable) -> Callable:
        span_name = name or f"tool.{func.__name__}"
        allow = {x.lower() for x in arg_allowlist} if arg_allowlist else None
        deny = {x.lower() for x in arg_denylist} if arg_denylist else set()
        redact = set(x.lower() for x in redact_keys)

        def _add_arg_attributes(span, bound_args: dict[str, Any]):
            for k, v in bound_args.items():
                kl = k.lower()
                if k.startswith("_"):
                    continue
                if allow is not None and kl not in allow:
                    continue
                if kl in deny:
                    continue
                if _should_redact(kl, v, redact):
                    span.set_attribute(f"{attribute_prefix}.arg.{k}", "***")
                else:
                    span.set_attribute(
                        f"{attribute_prefix}.arg.{k}", _truncate(v, max_len=max_value_len)
                    )

        def _enrich_with_ctx(span, bound_args: dict[str, Any]):
            ctx = bound_args.get("ctx") or bound_args.get("context")
            if ctx is None:
                return
            for key in ("request_id", "session_id", "client", "protocol_version"):
                val = getattr(ctx, key, None)
                if val:
                    span.set_attribute(
                        f"{attribute_prefix}.ctx.{key}", _truncate(val, max_value_len)
                    )

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def awrapper(*args, **kwargs):
                with _tracer.start_as_current_span(span_name, kind=kind) as span:
                    span.set_attribute(f"{attribute_prefix}.name", func.__name__)
                    bound = _bind_args(func, args, kwargs)
                    _add_arg_attributes(span, bound)
                    _enrich_with_ctx(span, bound)
                    try:
                        span.add_event("start")
                        result = await func(*args, **kwargs)
                        if capture_return_len:
                            span.set_attribute(
                                f"{attribute_prefix}.return_length",
                                len(str(result)) if result is not None else 0,
                            )
                        span.add_event("finish", {"status": "ok"})
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)[:200]))
                        span.add_event("finish", {"status": "error"})
                        raise

            return awrapper
        else:

            @wraps(func)
            def swrapper(*args, **kwargs):
                with _tracer.start_as_current_span(span_name, kind=kind) as span:
                    span.set_attribute(f"{attribute_prefix}.name", func.__name__)
                    bound = _bind_args(func, args, kwargs)
                    _add_arg_attributes(span, bound)
                    _enrich_with_ctx(span, bound)
                    try:
                        span.add_event("start")
                        result = func(*args, **kwargs)
                        if capture_return_len:
                            span.set_attribute(
                                f"{attribute_prefix}.return_length",
                                len(str(result)) if result is not None else 0,
                            )
                        span.add_event("finish", {"status": "ok"})
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)[:200]))
                        span.add_event("finish", {"status": "error"})
                        raise

            return swrapper

    return decorator
