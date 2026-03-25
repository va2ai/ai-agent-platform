from __future__ import annotations

import time
from typing import Any, AsyncIterator

from pydantic import BaseModel

from ..base import LLMClient, LLMResponse


class GeminiProvider(LLMClient):
    """Google Gemini provider using the google-genai SDK.

    Latest models (as of 2025):
    - gemini-3.1-pro-preview — most advanced, complex reasoning + agentic coding
    - gemini-3-flash-preview — frontier-class performance at low cost
    - gemini-3.1-flash-lite-preview — lightweight, fastest option
    - gemini-2.5-pro — stable, deep reasoning and coding
    - gemini-2.5-flash — stable, low-latency high-volume tasks

    Embedding:
    - gemini-embedding-2-preview — multimodal embeddings
    """

    provider_name = "gemini"

    def __init__(self, api_key: str, default_model: str = "gemini-3.1-pro-preview") -> None:
        from google import genai
        self._client = genai.Client(api_key=api_key)
        self._default_model = default_model

    async def generate(self, prompt: str, *, system: str = "", model: str | None = None, temperature: float = 0.7, max_tokens: int = 4096, **kwargs: Any) -> LLMResponse:
        from google.genai import types

        start = time.monotonic()
        config = types.GenerateContentConfig(
            system_instruction=system or None,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        response = self._client.models.generate_content(
            model=model or self._default_model,
            contents=prompt,
            config=config,
        )
        elapsed = (time.monotonic() - start) * 1000

        return LLMResponse(
            content=response.text or "",
            model=model or self._default_model,
            provider=self.provider_name,
            input_tokens=getattr(response.usage_metadata, "prompt_token_count", 0) if response.usage_metadata else 0,
            output_tokens=getattr(response.usage_metadata, "candidates_token_count", 0) if response.usage_metadata else 0,
            latency_ms=elapsed,
        )

    async def generate_structured(self, prompt: str, schema: type[BaseModel], *, system: str = "", model: str | None = None, **kwargs: Any) -> BaseModel:
        from google.genai import types

        start = time.monotonic()
        config = types.GenerateContentConfig(
            system_instruction=system or None,
            response_mime_type="application/json",
            response_schema=schema,
        )
        response = self._client.models.generate_content(
            model=model or self._default_model,
            contents=prompt,
            config=config,
        )
        return schema.model_validate_json(response.text)

    async def stream(self, prompt: str, *, system: str = "", model: str | None = None, **kwargs: Any) -> AsyncIterator[str]:
        from google.genai import types

        config = types.GenerateContentConfig(
            system_instruction=system or None,
        )
        for chunk in self._client.models.generate_content_stream(
            model=model or self._default_model,
            contents=prompt,
            config=config,
        ):
            if chunk.text:
                yield chunk.text

    async def embed(self, texts: list[str], *, model: str | None = None) -> list[list[float]]:
        result = self._client.models.embed_content(
            model=model or "gemini-embedding-2-preview",
            contents=texts,
        )
        return [e.values for e in result.embeddings]
