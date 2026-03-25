from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class VectorRecord(BaseModel):
    id: str
    vector: list[float]
    text: str
    metadata: dict[str, Any] = {}


class SearchResult(BaseModel):
    id: str
    text: str
    score: float
    metadata: dict[str, Any] = {}


class VectorStore(ABC):
    """Unified vector store interface. Backend-agnostic."""

    store_name: str = "base"

    @abstractmethod
    async def upsert(self, collection: str, records: list[VectorRecord]) -> None:
        ...

    @abstractmethod
    async def search(self, collection: str, query_vector: list[float], k: int = 10, filters: dict[str, Any] | None = None) -> list[SearchResult]:
        ...

    @abstractmethod
    async def delete(self, collection: str, ids: list[str]) -> None:
        ...

    @abstractmethod
    async def create_collection(self, name: str, dimension: int) -> None:
        ...
