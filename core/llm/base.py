from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    raw_response: dict[str, Any] | None = None


class LLMClient(ABC):
    """Model-agnostic LLM interface. All providers implement this."""

    provider_name: str = "base"

    @abstractmethod
    async def generate(self, prompt: str, *, system: str = "", model: str | None = None, temperature: float = 0.7, max_tokens: int = 4096, **kwargs: Any) -> LLMResponse:
        ...

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: type[BaseModel], *, system: str = "", model: str | None = None, **kwargs: Any) -> BaseModel:
        ...

    @abstractmethod
    async def stream(self, prompt: str, *, system: str = "", model: str | None = None, **kwargs: Any) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def embed(self, texts: list[str], *, model: str | None = None) -> list[list[float]]:
        ...
