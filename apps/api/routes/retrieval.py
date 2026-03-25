from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["retrieval"])


@router.post("/retrieve")
async def retrieve(query: str, collection: str = "default", k: int = 5):
    # Placeholder — wire up RetrievalPipeline here
    return {"query": query, "collection": collection, "results": []}
