from __future__ import annotations

from typing import Any

from .base import LLMClient, LLMResponse


class ModelRouter:
    """Routes LLM calls to the appropriate provider."""

    def __init__(self) -> None:
        self._providers: dict[str, LLMClient] = {}
        self._default_provider: str = ""

    def register(self, name: str, client: LLMClient, *, default: bool = False) -> None:
        self._providers[name] = client
        if default or not self._default_provider:
            self._default_provider = name

    def get(self, provider: str | None = None) -> LLMClient:
        name = provider or self._default_provider
        if name not in self._providers:
            raise ValueError(f"Provider '{name}' not registered. Available: {list(self._providers)}")
        return self._providers[name]

    async def generate(self, prompt: str, *, provider: str | None = None, **kwargs: Any) -> LLMResponse:
        return await self.get(provider).generate(prompt, **kwargs)


model_router = ModelRouter()
