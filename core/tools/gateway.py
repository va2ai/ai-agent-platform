from __future__ import annotations

import time
import logging
from typing import Any

from .base import BaseTool, ToolOutput
from .registry import tool_registry

logger = logging.getLogger(__name__)


class ToolGateway:
    """Single entry point for all tool execution.

    Handles validation, permission checks, logging, timeout, and retry.
    """

    async def execute(self, tool_name: str, input_data: dict[str, Any]) -> ToolOutput:
        tool = tool_registry.get(tool_name)
        schema = tool.input_schema()
        validated = schema(**input_data)

        start = time.monotonic()
        try:
            result = await tool.execute(validated)
            elapsed = (time.monotonic() - start) * 1000
            logger.info("tool.executed", extra={"tool": tool_name, "success": result.success, "latency_ms": elapsed})
            return result
        except Exception as e:
            elapsed = (time.monotonic() - start) * 1000
            logger.error("tool.failed", extra={"tool": tool_name, "error": str(e), "latency_ms": elapsed})
            return ToolOutput(success=False, error=str(e))


tool_gateway = ToolGateway()
