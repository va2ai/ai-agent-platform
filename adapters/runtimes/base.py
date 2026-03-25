from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from pydantic import BaseModel


class RunResult(BaseModel):
    run_id: str
    agent_name: str
    status: str
    output: dict[str, Any]
    steps: list[dict[str, Any]] = []
    token_usage: dict[str, int] = {}
    latency_ms: float = 0.0


class AgentRuntime(ABC):
    """Framework-agnostic agent runtime interface.

    Implement this for CrewAI, LangGraph, AutoGen, or custom orchestrators.
    Your core business logic should depend on this interface, never on a
    specific framework directly.
    """

    runtime_name: str = "base"

    @abstractmethod
    async def run_task(self, agent_name: str, payload: dict[str, Any], context: dict[str, Any] | None = None) -> RunResult:
        ...

    @abstractmethod
    async def handoff(self, from_agent: str, to_agent: str, payload: dict[str, Any]) -> RunResult:
        ...

    @abstractmethod
    async def stream_events(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        ...

    @abstractmethod
    async def resume(self, run_id: str) -> RunResult:
        ...

    @abstractmethod
    async def cancel(self, run_id: str) -> None:
        ...
