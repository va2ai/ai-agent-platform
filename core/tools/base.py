from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ToolInput(BaseModel):
    """Override with specific input schema per tool."""
    pass


class ToolOutput(BaseModel):
    success: bool
    result: Any = None
    error: str | None = None


class BaseTool(ABC):
    """Base class for all tools. Every tool goes through the tool gateway."""

    name: str = "base_tool"
    description: str = ""
    safety_level: str = "safe"  # safe | requires_approval | restricted
    timeout_seconds: int = 30
    max_retries: int = 2

    @abstractmethod
    def input_schema(self) -> type[BaseModel]:
        """Return the Pydantic model for this tool's input."""
        ...

    @abstractmethod
    async def execute(self, input_data: BaseModel) -> ToolOutput:
        """Execute the tool with validated input."""
        ...
