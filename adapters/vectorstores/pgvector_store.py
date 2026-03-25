from __future__ import annotations

from typing import Any

from .base import VectorStore, VectorRecord, SearchResult


class PgVectorStore(VectorStore):
    store_name = "pgvector"

    def __init__(self, connection_string: str) -> None:
        self._conn_str = connection_string
        self._pool = None

    async def _get_pool(self):
        if self._pool is None:
            import asyncpg
            self._pool = await asyncpg.create_pool(self._conn_str)
        return self._pool

    async def create_collection(self, name: str, dimension: int) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id TEXT PRIMARY KEY,
                    embedding vector({dimension}),
                    text TEXT,
                    metadata JSONB DEFAULT '{{}}'::jsonb
                )
            """)

    async def upsert(self, collection: str, records: list[VectorRecord]) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            for record in records:
                await conn.execute(f"""
                    INSERT INTO {collection} (id, embedding, text, metadata)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (id) DO UPDATE SET embedding = $2, text = $3, metadata = $4
                """, record.id, str(record.vector), record.text, record.metadata)

    async def search(self, collection: str, query_vector: list[float], k: int = 10, filters: dict[str, Any] | None = None) -> list[SearchResult]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT id, text, metadata, 1 - (embedding <=> $1::vector) AS score
                FROM {collection}
                ORDER BY embedding <=> $1::vector
                LIMIT $2
            """, str(query_vector), k)
            return [SearchResult(id=row["id"], text=row["text"], score=float(row["score"]), metadata=row["metadata"] or {}) for row in rows]

    async def delete(self, collection: str, ids: list[str]) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(f"DELETE FROM {collection} WHERE id = ANY($1)", ids)
