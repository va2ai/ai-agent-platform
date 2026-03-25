from __future__ import annotations

from typing import Any


class RetrievalPipeline:
    """Orchestrates embed -> search -> rerank."""

    def __init__(self, llm_client, vector_store, *, reranker=None) -> None:
        self._llm = llm_client
        self._store = vector_store
        self._reranker = reranker

    async def search(self, query: str, collection: str, k: int = 10, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        vectors = await self._llm.embed([query])
        results = await self._store.search(collection, vectors[0], k=k * 2 if self._reranker else k, filters=filters)
        hits = [{"id": r.id, "text": r.text, "score": r.score, "metadata": r.metadata} for r in results]
        if self._reranker:
            hits = await self._reranker.rerank(query, hits, k=k)
        return hits[:k]
