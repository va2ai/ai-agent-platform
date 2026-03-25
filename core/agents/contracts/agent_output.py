from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class StepRecord(BaseModel):
    step_number: int
    action: str
    tool_used: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: Any = None
    reasoning: str = ""


class AgentOutput(BaseModel):
    result: str
    status: str  # completed | failed | handoff
    steps: list[StepRecord] = []
    handoff_to: str | None = None
    handoff_payload: dict[str, Any] | None = None
    metadata: dict[str, Any] = {}
