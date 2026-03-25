"""In-memory vector store for testing RAG without external dependencies."""
from __future__ import annotations

import hashlib
import math
from typing import Any


class MockSearchResult:
    def __init__(self, id: str, text: str, score: float, metadata: dict[str, Any] = None):
        self.id = id
        self.text = text
        self.score = score
        self.metadata = metadata or {}


class MockVectorStore:
    """In-memory vector store with cosine similarity search."""

    store_name = "mock"

    def __init__(self) -> None:
        self._collections: dict[str, list[dict]] = {}

    def _hash_embed(self, text: str, dim: int = 384) -> list[float]:
        """Deterministic embedding from text hash."""
        hash_bytes = hashlib.sha256(text.encode()).digest()
        vector = []
        for i in range(dim):
            byte_val = hash_bytes[i % len(hash_bytes)]
            vector.append((byte_val / 255.0) * 2 - 1)
        return vector

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    async def create_collection(self, name: str, dimension: int = 384) -> None:
        self._collections[name] = []

    async def upsert(self, collection: str, records: list[dict]) -> None:
        if collection not in self._collections:
            self._collections[collection] = []
        for record in records:
            self._collections[collection].append(record)

    async def search(self, collection: str, query_vector: list[float], k: int = 5, **kwargs) -> list[MockSearchResult]:
        if collection not in self._collections:
            return []

        scored = []
        for record in self._collections[collection]:
            score = self._cosine_similarity(query_vector, record["vector"])
            scored.append((score, record))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            MockSearchResult(
                id=record["id"],
                text=record["text"],
                score=score,
                metadata=record.get("metadata", {}),
            )
            for score, record in scored[:k]
        ]

    async def delete(self, collection: str, ids: list[str]) -> None:
        if collection in self._collections:
            self._collections[collection] = [
                r for r in self._collections[collection] if r["id"] not in ids
            ]
