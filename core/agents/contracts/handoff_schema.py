from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HandoffPayload(BaseModel):
    from_agent: str
    to_agent: str
    reason: str
    context: dict[str, Any] = {}
    conversation_history: list[dict[str, str]] = []
    partial_result: str | None = None
