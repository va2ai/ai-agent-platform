from __future__ import annotations

import uuid
import time
from typing import Any, AsyncIterator

from .base import AgentRuntime, RunResult


class CustomRuntime(AgentRuntime):
    """Simple custom runtime — no external framework dependency.

    Implements a basic agent loop: prompt -> LLM -> tool calls -> repeat until done.
    Replace or extend this with your own orchestration logic.
    """

    runtime_name = "custom"

    def __init__(self, llm_client, tool_gateway=None) -> None:
        self._llm = llm_client
        self._tools = tool_gateway

    async def run_task(self, agent_name: str, payload: dict[str, Any], context: dict[str, Any] | None = None) -> RunResult:
        run_id = str(uuid.uuid4())
        start = time.monotonic()
        ctx = context or {}

        system_prompt = ctx.get("system_prompt", "You are a helpful assistant.")
        task = payload.get("task", "")

        response = await self._llm.generate(task, system=system_prompt)

        elapsed = (time.monotonic() - start) * 1000
        return RunResult(run_id=run_id, agent_name=agent_name, status="completed", output={"result": response.content}, token_usage={"input": response.input_tokens, "output": response.output_tokens}, latency_ms=elapsed)

    async def handoff(self, from_agent: str, to_agent: str, payload: dict[str, Any]) -> RunResult:
        return await self.run_task(to_agent, payload)

    async def stream_events(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        yield {"event": "complete", "run_id": run_id}

    async def resume(self, run_id: str) -> RunResult:
        raise NotImplementedError("Resume not supported in custom runtime")

    async def cancel(self, run_id: str) -> None:
        pass
