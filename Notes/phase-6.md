# Phase 6 Notes — RAG (Retrieval-Augmented Generation)

## What you learn in this phase

This phase teaches you how to connect an LLM to your own documents so it can answer questions with grounded context instead of relying only on its training data.

## Core ideas

- Embeddings: convert text into vectors so similar meanings can be found
- Chunking: split large documents into smaller pieces for better retrieval
- Retrieval: find the most relevant chunks for a question
- Prompting: place retrieved context into the prompt so the model answers using evidence
- Evaluation: measure whether the retrieved context and the final answer are useful
- Conversational RAG: keep recent history so follow-up questions work better

## Typical RAG pipeline

1. Load documents
2. Chunk them
3. Create embeddings
4. Store or index them
5. Retrieve relevant chunks
6. Build a prompt with those chunks
7. Send that prompt to an LLM
8. Return the generated answer

## Important engineering concepts

- Semantic search vs keyword search
- Hybrid search
- Reranking
- Context window limits
- Hallucination reduction
- Prompt grounding
- Evaluation of retrieval quality

## Practical examples in this phase

- Embeddings basics
- Chunking strategies
- Semantic search
- Vector database concepts
- Hybrid search
- Reranking
- Conversational RAG
- Real LLM integration through Ollama
- Simple API wrapper with FastAPI

## How to run the project

```bash
pip install -r requirements.txt
python 6-RAG/03-pipelines/04-real-llm-integration.py
```

If you want a web interface, you can also run:

```bash
uvicorn app.api:app --reload
```

Then visit:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## Why this matters

RAG is one of the most practical AI engineering skills because it allows you to build systems that use private documents, reduce hallucinations, and answer questions more reliably than a plain LLM alone.
