from __future__ import annotations

import logging
import time
from typing import Any, Callable

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AgentEvent(BaseModel):
    event_type: str  # agent.start, agent.complete, tool.call, llm.call, etc.
    run_id: str
    agent_name: str = ""
    step_name: str = ""
    timestamp: float = 0.0
    data: dict[str, Any] = {}

    def __init__(self, **kwargs):
        if "timestamp" not in kwargs:
            kwargs["timestamp"] = time.time()
        super().__init__(**kwargs)


class EventBus:
    """Central event bus for observability. All workflow steps emit events here."""

    def __init__(self) -> None:
        self._handlers: list[Callable[[AgentEvent], None]] = []

    def subscribe(self, handler: Callable[[AgentEvent], None]) -> None:
        self._handlers.append(handler)

    def emit(self, event: AgentEvent) -> None:
        logger.debug("event.emitted", extra={"event_type": event.event_type, "run_id": event.run_id})
        for handler in self._handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error("event.handler_error", extra={"error": str(e)})


event_bus = EventBus()
