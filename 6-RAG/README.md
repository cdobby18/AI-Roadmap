# Phase 6 — RAG + LangChain + LangGraph + Agents

**Status: ⬜ Upcoming**

> Most employable AI engineering skill right now

## What this phase will cover

- Vector DBs: ChromaDB locally, embed sentences, query nearest neighbor
- Chunking: ~500 token chunks with overlap before embedding
- RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- LangChain chains: loaders, splitters, embeddings, retriever, LLM
- Conversational RAG: memory for multi-turn history
- **LangGraph agents**: stateful agents with nodes, edges, conditional routing
- **Model Context Protocol (MCP)**: connect agents to external tools
- **LangSmith tracing**: trace the full RAG pipeline, see exactly where retrieval fails
- **Redis cache**: cache embeddings to reduce API calls and latency
- **RAGAS evaluation**: faithfulness, answer relevancy, context precision

## Builds on

- Phase 4's [Vivre Card](../Projects/phase-4-vivre-card/) project — embedding + cosine-similarity search is the mechanical core of RAG retrieval
- Phase 5 (LLM APIs, tool calling) — the generation half of retrieve-then-generate
