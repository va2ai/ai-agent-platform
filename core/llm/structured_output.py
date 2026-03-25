from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from .base import LLMClient

T = TypeVar("T", bound=BaseModel)


async def generate_structured(client: LLMClient, prompt: str, schema: type[T], *, system: str = "", **kwargs) -> T:
    """Convenience function for structured generation with validation."""
    result = await client.generate_structured(prompt, schema, system=system, **kwargs)
    if not isinstance(result, schema):
        raise TypeError(f"Expected {schema.__name__}, got {type(result).__name__}")
    return result
