from __future__ import annotations

from enum import Enum


class LLMProvider(str, Enum):
    GEMINI = "gemini"


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    HANDOFF = "handoff"


class ToolSafetyLevel(str, Enum):
    SAFE = "safe"
    REQUIRES_APPROVAL = "requires_approval"
    RESTRICTED = "restricted"
