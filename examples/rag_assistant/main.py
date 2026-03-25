"""RAG (Retrieval-Augmented Generation) demo with mock providers.

Run: python examples/rag_assistant/main.py

No API keys or external services required.
"""
from __future__ import annotations

import asyncio

from .mock_vectorstore import MockVectorStore
from ..simple_chat.mock_provider import MockLLMClient


SAMPLE_DOCS = [
    {
        "id": "doc-1",
        "text": "FastAPI is a modern web framework for building APIs with Python. It is based on standard Python type hints and provides automatic data validation, serialization, and interactive documentation.",
        "metadata": {"source": "docs", "topic": "fastapi"},
    },
    {
        "id": "doc-2",
        "text": "Vector databases store high-dimensional vectors for similarity search. Popular options include pgvector (PostgreSQL extension), Qdrant, Pinecone, and Chroma. They enable semantic search over documents.",
        "metadata": {"source": "docs", "topic": "vector-db"},
    },
    {
        "id": "doc-3",
        "text": "Multi-agent systems use multiple AI agents that collaborate to solve complex tasks. Each agent can have specialized capabilities, tools, and knowledge.",
        "metadata": {"source": "docs", "topic": "agents"},
    },
    {
        "id": "doc-4",
        "text": "Observability for AI systems tracks token usage, latency, cost per request, tool call success rates, and retrieval quality scores. This enables debugging, optimization, and cost management.",
        "metadata": {"source": "docs", "topic": "observability"},
    },
]


async def main():
    llm = MockLLMClient()
    store = MockVectorStore()

    print("=" * 60)
    print("  RAG Assistant — Mock Providers Demo")
    print("=" * 60)

    print("\n1. Creating vector collection...")
    await store.create_collection("knowledge", dimension=384)

    print("2. Ingesting sample documents...")
    records = []
    for doc in SAMPLE_DOCS:
        embedding = (await llm.embed([doc["text"]]))[0]
        records.append({
            "id": doc["id"],
            "vector": embedding,
            "text": doc["text"],
            "metadata": doc["metadata"],
        })
    await store.upsert("knowledge", records)
    print(f"   Ingested {len(records)} documents")

    print("\n3. Ask questions (type 'quit' to exit):")
    print("   Try: 'What are vector databases?', 'How does observability work?'")
    print()

    while True:
        try:
            query = input("Q: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        query_vec = (await llm.embed([query]))[0]
        results = await store.search("knowledge", query_vec, k=3)

        print(f"\n   Retrieved {len(results)} relevant chunks:")
        for i, r in enumerate(results):
            print(f"   [{i+1}] (score: {r.score:.3f}) {r.text[:80]}...")

        context = "\n\n".join([f"[Source: {r.metadata.get('topic', 'unknown')}] {r.text}" for r in results])

        response = await llm.generate(
            f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {query}",
            system="You are a helpful assistant that answers questions based on provided context.",
        )

        print(f"\nA: {response.content}")
        print(f"   [{response.input_tokens} in / {response.output_tokens} out tokens]")
        print()


if __name__ == "__main__":
    asyncio.run(main())
