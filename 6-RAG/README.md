# Phase 6 — RAG (Retrieval-Augmented Generation)

**Status: ⬜ Upcoming**

> This phase teaches you how to build systems that let an LLM answer questions using your own documents instead of relying only on its training data.

## What this project is about

RAG stands for Retrieval-Augmented Generation. The idea is simple:

1. Take a set of documents.
2. Split them into smaller chunks.
3. Convert those chunks into embeddings.
4. Store them in a searchable structure.
5. When a user asks a question, retrieve the most relevant chunks.
6. Send those chunks to the LLM as context.
7. Ask the model to answer based on that context.

This is what makes the system more accurate, grounded, and useful for real-world knowledge bases.

---

## Core concepts

### 1. Embeddings
Embeddings are numerical representations of text. They allow the system to measure semantic similarity between pieces of text.

Why it matters:
- Similar meanings become close in vector space.
- The model can find relevant content even if the wording is different.

### 2. Chunking
Documents are usually too large to send as-is to a model. Chunking splits them into smaller, meaningful pieces.

Why it matters:
- Better retrieval precision
- Lower token cost
- Easier context management

### 3. Retrieval
Retrieval is the step where the system finds the most relevant chunks for a user query.

Why it matters:
- It provides grounded context to the model
- It reduces hallucinations

### 4. Hybrid search and reranking
A strong RAG system often combines:
- keyword search for exact matches
- semantic search for meaning-based matches
- reranking to improve the final order of results

Why it matters:
- Better retrieval quality
- More robust question answering

### 5. Prompting with context
Once relevant chunks are found, they are inserted into the prompt so the model can answer using that evidence.

Why it matters:
- The answer becomes more factual
- The system becomes more explainable

### 6. Conversational memory
In real chat applications, the system should remember earlier turns so the latest answer can use both current context and conversation history.

Why it matters:
- Better multi-turn experience
- More coherent assistant behavior

### 7. Evaluation
A RAG system should be evaluated for:
- whether the right context was retrieved
- whether the answer is faithful to that context
- whether the answer is relevant to the question
- whether retrieval quality degrades on harder queries

---

## How the project works

The project is organized as a mini RAG pipeline.

### System flow

```text
User Question
   ↓
Load documents from data/raw
   ↓
Split documents into chunks
   ↓
Create or use embeddings
   ↓
Retrieve relevant chunks
   ↓
Build prompt with retrieved context
   ↓
Send prompt to LLM
   ↓
Return grounded answer
```

---

## Project structure

```text
6-RAG/
├── 01-foundations/                # Core concepts
│   ├── 01-embeddings-basics.py
│   ├── 02-document-chunking.py
│   └── 03-document-loading-and-preprocessing.py
│
├── 02-retrieval/                  # Search and memory layer
│   ├── 01-semantic-search.py
│   ├── 02-vector-databases.py
│   ├── 03-hybrid-search.py
│   └── 04-reranking.py
│
├── 03-pipelines/                  # End-to-end RAG flow
│   ├── 01-basic-rag.py
│   ├── 02-prompt-engineering-for-rag.py
│   ├── 03-conversational-rag.py
│   └── 04-real-llm-integration.py
│
├── 04-evaluation/                 # Quality and reliability
│   ├── 01-ragas-intro.py
│   └── 02-metrics-and-debugging.py
│
├── app/                           # Reusable project code
│   ├── __init__.py
│   ├── rag_config.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── retriever.py
│   ├── rag_pipeline.py
│   ├── api.py
│   └── ollama_client.py
│
├── data/                          # Documents and processed chunks
│   ├── raw/
│   │   └── sample_docs/
│   └── processed/
│       └── chunks/
│
├── notebooks/                     # Exploratory experiments
├── tests/                         # Basic sanity checks
└── README.md
```

---

## How to run it

### 1. Install dependencies
From the repository root:

```bash
pip install -r requirements.txt
```

### 2. Run the basic embedding example
```bash
python 6-RAG/01-foundations/01-embeddings-basics.py
```

### 3. Run the chunking example
```bash
python 6-RAG/01-foundations/02-document-chunking.py
```

### 4. Run the semantic search example
```bash
python 6-RAG/02-retrieval/01-semantic-search.py
```

### 5. Run the basic RAG pipeline
```bash
python 6-RAG/03-pipelines/01-basic-rag.py
```

### 6. Run the prompt builder example
```bash
python 6-RAG/03-pipelines/02-prompt-engineering-for-rag.py
```

### 7. Run the evaluation example
```bash
python 6-RAG/04-evaluation/01-ragas-intro.py
```

### 8. Run the metrics example
```bash
python 6-RAG/04-evaluation/02-metrics-and-debugging.py
```

### 9. Run the real LLM integration example
```bash
python 6-RAG/03-pipelines/04-real-llm-integration.py
```

### 10. Run the project-style pipeline
```bash
python -m app.rag_pipeline
```

### 11. Run the FastAPI RAG endpoint
```bash
uvicorn app.api:app --reload
```

Then open:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

### 12. Connect to Ollama locally
Make sure Ollama is installed and running:

```bash
ollama serve
```

Then run the integration example:
```bash
python 6-RAG/03-pipelines/04-real-llm-integration.py
```

---

## What each part does

### Foundations
- Understand embeddings and similarity
- Learn how chunking works
- See why splitting text matters

### Retrieval
- Match a question to the most relevant pieces of text
- Combine semantic and keyword signals
- Improve ordering with reranking

### Pipelines
- Combine retrieval and prompting into one flow
- Build a simple question-answering system over your documents
- Support conversational follow-up questions
- Connect retrieved context to a real LLM for a complete RAG experience
- Wrap the flow in a small API so it behaves like a real product backend

### Evaluation
- Check whether retrieved chunks are useful
- Measure whether the final answer is grounded and relevant
- Analyze retrieval issues and debug failures

---

## Why this matters for AI engineering

RAG is one of the most practical AI engineering skills because it helps you build systems that:

- connect external documents to an LLM in a grounded way
- move from isolated retrieval logic to a real end-to-end AI application
- use private or domain-specific documents
- reduce hallucinations
- give more accurate answers
- work better than a plain LLM alone

This is the foundation for:
- chat with your documents
- internal knowledge assistants
- support copilots
- enterprise search tools
- domain-specific copilots

---

## Suggested learning path

1. Start with embeddings and chunking
2. Move to retrieval and vector search
3. Build a simple prompt-based RAG pipeline
4. Evaluate results and improve retrieval quality
5. Later upgrade to Chroma, FAISS, LangChain, and a real vector database

---

## Next: Phase 7 (Advanced Frameworks)

After you understand RAG, the next step is to learn more advanced orchestration tools such as:
- LangChain
- LangGraph
- LangSmith
- Guardrails
- MCP

See: [7-Advanced-Frameworks/README.md](../7-Advanced-Frameworks/README.md)
