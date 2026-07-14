# Phase 6 — RAG (Retrieval-Augmented Generation)

**Status: ⬜ Upcoming**

> Most employable AI engineering skill right now

## What this phase will cover

**RAG Fundamentals**
- Embeddings: converting text to vectors
- Vector databases: ChromaDB, FAISS, Pinecone, Weaviate
- Document chunking: strategies, overlap, optimal sizes
- Semantic search: finding relevant documents

**Building RAG Systems**
- RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- Basic RAG from scratch (no frameworks)
- RAG with LangChain: loaders, splitters, retrievers
- Conversational RAG: memory for multi-turn history

**Integration**
- Redis caching: reduce API calls and latency
- Hybrid search: combine keyword + semantic search
- Reranking: improve retrieval quality
- RAGAS evaluation: faithfulness, answer relevancy, context precision

## Files (To Be Created)

```
01-embeddings.py                 - Generate & understand embeddings
02-vector-databases.py           - Store & search with vector DBs
03-document-chunking.py          - Split documents strategically
04-semantic-search.py            - Similarity search basics
05-basic-rag-from-scratch.py     - Build RAG without frameworks
06-rag-with-langchain.py         - RAG using LangChain
07-conversational-rag.py         - Multi-turn RAG with memory
08-hybrid-search.py              - Combine keyword + semantic
09-rag-evaluation.py             - RAGAS evaluation
```

## Next: Phase 7 (Advanced Frameworks)

After mastering RAG, learn advanced orchestration:

**Phase 7 covers:**
- LangChain advanced patterns (agents, complex chains)
- LangGraph: multi-step agentic workflows
- LangSmith: tracing, evaluation, experimentation
- Advanced guardrails & output validation
- MCP (Model Context Protocol)

See: [7-Advanced-Frameworks/README.md](../7-Advanced-Frameworks/README.md)

## Builds on

- Phase 4's [Vivre Card](../Projects/phase-4-vivre-card/) project — embedding + cosine-similarity search
- Phase 5 (LLM APIs, tool calling) — the generation half of retrieve-then-generate
