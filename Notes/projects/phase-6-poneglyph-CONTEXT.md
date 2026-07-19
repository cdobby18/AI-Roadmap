# Poneglyph Reader — Project Context

## What Is It?

A **RAG (Retrieval-Augmented Generation)** application that lets you chat with the One Piece wiki. Built on the Phase 6 RAG pipeline.

## Why This Matters

RAG is the most widely deployed LLM pattern in production:
- **ChatGPT browsing** = RAG over the web
- **Notion AI Q&A** = RAG over your notes
- **Glean / Perplexity** = RAG over indexed documents
- **Customer support bots** = RAG over knowledge bases

Building this teaches you the entire stack — from scraping raw data to deploying a chat interface.

## Architecture

```
User question
    │
    ▼
┌────────────────┐
│ Query Rewrite  │ ← LLM rewrites follow-ups as standalone queries
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Vector Search  │ ← ChromaDB with MiniLM-L6-v2 embeddings
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Reranker     │ ← cross-encoder/ms-marco re-ranks top chunks
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  LLM Generate  │ ← Ollama (llama2) answers with [Source N] citations
└───────┬────────┘
        │
        ▼
   Answer + Sources
```

## Modules

| File | Role |
|------|------|
| `scraper.py` | Fetch + parse One Piece wiki pages (HTML → clean text) |
| `ingestion.py` | Chunk → embed → store in ChromaDB |
| `rag.py` | Rewrite → search → rerank → generate |
| `app.py` | Streamlit chat UI |

## How It Connects to Phase 6

- `6-RAG/01-foundations/01-embeddings-basics.py` → embedding concepts used in `ingestion.py`
- `6-RAG/02-retrieval/03-hybrid-search.py` → search strategies refined in `rag.py`
- `6-RAG/02-retrieval/04-reranking.py` → cross-encoder reranking used in `rag.py`
- `6-RAG/03-pipelines/05-query-rewriting.py` → query rewriting used in `rag.py`
- `6-RAG/app/chroma_store.py` → ChromaDB pattern reused in `ingestion.py`

## Run

```bash
cd Projects/phase-6-poneglyph
pip install -r requirements.txt
python -m streamlit run app.py
```
