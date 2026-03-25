from __future__ import annotations


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class LLMError(AppError):
    """LLM provider error."""

    def __init__(self, message: str, provider: str = "unknown") -> None:
        self.provider = provider
        super().__init__(message, code="LLM_ERROR")


class ToolError(AppError):
    """Tool execution error."""

    def __init__(self, message: str, tool_name: str = "unknown") -> None:
        self.tool_name = tool_name
        super().__init__(message, code="TOOL_ERROR")


class RetrievalError(AppError):
    """Vector retrieval error."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="RETRIEVAL_ERROR")
