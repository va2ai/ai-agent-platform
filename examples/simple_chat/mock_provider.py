"""Mock LLM provider for testing without API keys."""
from __future__ import annotations

import time
from typing import Any, AsyncIterator


class LLMResponse:
    """Standalone response model for the mock (avoids import issues in examples)."""
    def __init__(self, content: str, model: str = "mock", provider: str = "mock",
                 input_tokens: int = 0, output_tokens: int = 0, latency_ms: float = 0.0):
        self.content = content
        self.model = model
        self.provider = provider
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.latency_ms = latency_ms


class MockLLMClient:
    """Mock LLM that returns canned responses. Implements the LLMClient interface."""

    provider_name = "mock"

    RESPONSES = {
        "hello": "Hello! I'm a mock AI assistant. How can I help you today?",
        "help": "I can help with: answering questions, summarizing text, and explaining concepts. (This is a mock response.)",
        "default": "That's an interesting question! As a mock provider, I don't have real AI capabilities, but in production this would be handled by Gemini 2.5 Pro.",
    }

    async def generate(self, prompt: str, *, system: str = "", model: str | None = None,
                       temperature: float = 0.7, max_tokens: int = 4096, **kwargs: Any) -> LLMResponse:
        start = time.monotonic()
        prompt_lower = prompt.lower().strip()

        content = self.RESPONSES.get(prompt_lower, self.RESPONSES["default"])
        if system:
            content = f"[System: {system[:50]}...] {content}"

        elapsed = (time.monotonic() - start) * 1000
        input_tokens = len(prompt.split())
        output_tokens = len(content.split())

        return LLMResponse(
            content=content,
            model="mock-model",
            provider="mock",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=elapsed,
        )

    async def generate_structured(self, prompt: str, schema, *, system: str = "", **kwargs) -> Any:
        """Return a mock structured response."""
        response = await self.generate(prompt, system=system)
        return {"result": response.content}

    async def stream(self, prompt: str, *, system: str = "", **kwargs) -> AsyncIterator[str]:
        response = await self.generate(prompt, system=system)
        words = response.content.split()
        for word in words:
            yield word + " "

    async def embed(self, texts: list[str], *, model: str | None = None) -> list[list[float]]:
        """Return deterministic fake embeddings based on text hash."""
        import hashlib
        embeddings = []
        for text in texts:
            hash_bytes = hashlib.sha256(text.encode()).digest()
            vector = []
            for i in range(384):
                byte_val = hash_bytes[i % len(hash_bytes)]
                vector.append((byte_val / 255.0) * 2 - 1)
            embeddings.append(vector)
        return embeddings
