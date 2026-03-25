from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AgentInput(BaseModel):
    task: str
    context: dict[str, Any] = {}
    tools_available: list[str] = []
    constraints: list[str] = []
    max_steps: int = 10
    session_id: str | None = None
