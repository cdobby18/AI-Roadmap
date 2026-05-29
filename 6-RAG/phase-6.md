# Phase 6 · RAG + LangChain + Agents

---

## What You'll Learn

- **Why RAG Exists** — LLMs hallucinate on facts they weren't trained on. RAG grounds responses in real documents. Understand the problem before the solution.
- **Vector Databases** — embeddings stored as vectors, similarity search (cosine, dot product). ChromaDB to start, know that Pinecone/Weaviate exist for production scale.
- **Document Chunking** — why you can't just feed a whole PDF into an LLM. Chunk size (~500 tokens), overlap (~50 tokens), and why both matter for retrieval quality.
- **Full RAG Pipeline** — ingest → chunk → embed → store → retrieve → generate. Know every step and what can break at each one.
- **Conversational RAG** — add memory so the chatbot understands follow-up questions in context.
- **LangChain** — chains, document loaders, retrievers, prompt templates. The glue of most AI pipelines.
- **LangGraph** — stateful agents with graph-based control flow. This is the production-grade way to build agents with loops, conditions, and memory.
- **Model Context Protocol (MCP)** — how agents call external tools (APIs, databases, search). The emerging standard for tool use.
- **Redis Embedding Cache** — don't re-embed the same documents on every run. Cache embeddings, save time and cost.
- **RAGAS Evaluation** — measure your RAG system properly: faithfulness, answer relevancy, context precision, context recall. Vibes are not a metric.

---

## Resources

| Resource | What You Get | Format | Cost |
|----------|-------------|--------|------|
| LangChain docs (python.langchain.com) | Official reference. Read the RAG and retrieval sections thoroughly. | Docs | Free |
| LangGraph docs (langchain-ai.github.io/langgraph) | The production agent framework. Work through all quickstart examples. | Docs | Free |
| Greg Kamradt — LangChain cookbook (YouTube) | Practical LangChain walkthroughs. Chunking strategy video is essential. | Video | Free |
| ChromaDB docs (trychroma.com) | Set up a local vector DB in minutes. Read the quickstart and cookbook. | Docs | Free |
| RAGAS docs (docs.ragas.io) | Evaluation framework for RAG. Required — don't ship without metrics. | Docs | Free |
| Pinecone — "What is RAG?" (learning.pinecone.io) | Best written RAG explainer. Read before building. | Article | Free |
| Redis docs — caching basics | Understand how to cache embeddings. Don't re-embed on every run. | Docs | Free |

---
