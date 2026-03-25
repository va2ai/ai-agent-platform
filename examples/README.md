# Examples

## Simple Chat

A single-agent chat loop using a mock LLM provider. No API keys required.

```bash
python examples/simple_chat/main.py
```

## RAG Assistant

A retrieval-augmented generation demo: ingest sample documents, embed them, search, and answer questions. Uses an in-memory mock vector store.

```bash
python examples/rag_assistant/main.py
```

Both examples use mock providers so you can verify the architecture works before connecting real APIs.
