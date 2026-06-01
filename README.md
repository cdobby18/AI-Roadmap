# 🤖 AI Engineering Roadmap

This repository documents my structured, project-driven journey toward becoming a
**Junior AI Engineer** — from Python foundations all the way to deploying production
RAG systems and AI agents.

**From Zero to AI Engineer — one built project at a time.**

---

## The Path

```
ai-engineer/
│
├── 01 · Python Foundations + SQL
│     ├── OOP + Exceptions
│     ├── File I/O + APIs
│     └── SQL + SQLite
│
├── 02 · FastAPI + Auth + Security
│     ├── Routes + Pydantic
│     ├── JWT Auth
│     └── Rate Limiting
│
├── 03 · Machine Learning + W&B
│     ├── scikit-learn + PyTorch
│     └── Experiment Tracking
│
├── 04 · NLP Fundamentals + Transformers 
│     ├── Tokenization + Embeddings
│     └── Fine-tuning
│     ├── Attention Mechanism
│     └── BERT vs GPT
│
├── 05· LLMs + Prompt Engineering + Observability
│     ├── Prompting Techniques
│     └── LangSmith + Langfuse
│
├── 06 · RAG + LangChain + LangGraph + Agents
│     ├── Vector DBs + Chunking
│     ├── LangChain + LangGraph
│     └── RAGAS Evaluation
│
├── 07 · Deploy + CI/CD + Portfolio
│     ├── Docker + GitHub Actions
│     └── HuggingFace Spaces
│
├── 08 · Projects
│     ├── Personal Projects per Phase

```

---

## 📊 Progress

| Phase | Topic | Status |
|-------|-------|--------|
| 1 | Python Foundations + SQL | ✅ Complete |
| 2 | FastAPI + Security Basics | 🔄 In Progress |
| 3 | Machine Learning + W&B Tracking | ⬜ Upcoming |
| 4 | NLP Fundamentals + Transformers | ⬜ Upcoming |
| 5 | LLMS + Prompt Engineering + Observability | ⬜ Upcoming |
| 6 | RAG + LangChain + LangGraph + Agents | ⬜ Upcoming |
| 7 | Deploy + CI/CD + Portfolio | ⬜ Upcoming |
| 8 | Projects | ⬜ Upcoming |

---

## Phase Breakdown

### Phase 1 — Python Foundations + SQL
**Status: ✅ Complete**

- OOP: classes, `__init__`, `self`, inheritance, magic methods
- Exceptions: `try/except/finally` — handle errors, not just print them
- File I/O: read/write text, CSV, JSON
- API requests: `requests` library, handle responses
- Modules and packages: `__init__.py`, importing your own code
- SQL basics: `SELECT`, `WHERE`, `JOIN`, `GROUP BY` using SQLite *(3-day module)*

---

### Phase 2 — FastAPI + Security Basics
**Status: 🔄 In Progress**

> FastAPI chosen over Flask for its async support, automatic Swagger docs,
> and native Pydantic integration — all critical for production AI backends.

- Why FastAPI: async support, automatic docs, Pydantic validation
- GET and POST endpoints returning JSON
- Pydantic models for request validation — critical for AI APIs
- Async endpoints: `async/await` and why it matters
- Path params, query params, request bodies
- **JWT authentication** — protect endpoints with `python-jose` + `passlib`
- **Rate limiting** — `slowapi`, 10 requests/minute per user
- Environment variables: `Pydantic Settings` + `.env` files

---

### Phase 3 — Machine Learning + Experiment Tracking
**Status: ⬜ Upcoming**

> NumPy and Pandas are learned here in context — not as a separate phase

- scikit-learn: train/test split, cross-validation, pipelines, metrics
- PyTorch: tensors, autograd, training loop — forward pass, loss, backward, optimizer
- `nn.Module` — build and understand every line of a neural network
- HuggingFace `pipeline()` for inference in 5 lines
- Evaluate properly: confusion matrix, never evaluate on training data
- **W&B experiment tracking** — log accuracy, loss, hyperparameters from day 1
- Gradio: wrap model in a demo UI, publish to HuggingFace Spaces

---

### Phase 4 — NLP Fundamentals
**Status: ⬜ Upcoming**

- Tokenization: LLMs read tokens, not words — inspect tokenizer output
- Word embeddings: Word2Vec — a word as a list of numbers encoding meaning
- TF-IDF: implement from scratch, understand when to use vs embeddings
- NLP tasks: sentiment analysis, NER, summarization via HuggingFace
- Fine-tuning: HuggingFace `Trainer` on a custom dataset
- Encoder (BERT) vs decoder (GPT) — conceptual understanding before Phase 5

---

### Phase 5 — Transformers: How They Actually Work
**Status: ⬜ Upcoming**

> Dedicated phase added based on mentor recommendation — before LLMs,
> understand the architecture

- Attention mechanism: every token attends to every other token simultaneously
- Self-attention: queries, keys, values — what they are and why the math works
- Multi-head attention: running attention in parallel
- Positional encoding: how transformers encode order without recurrence
- Encoder-only (BERT) vs decoder-only (GPT)
- Read *Attention Is All You Need* — abstract + architecture section minimum

---

### Phase 6 — LLMs + Prompt Engineering + Observability
**Status: ⬜ Upcoming**

- Tokens, context window, temperature — know these cold
- Zero-shot, few-shot, chain-of-thought prompting — implement and compare all three
- System prompts: shape model behavior across all turns
- Function/tool calling: the LLM decides when to call your Python function
- Structured outputs: force valid JSON using native API support
- **LangSmith / Langfuse** — trace every LLM call: latency, token usage, errors
- **Prompt injection** — understand the attack, implement input sanitization
- Ollama: run models locally (llama3, mistral) — reduce API costs while learning
- Serve chatbot as a proper async FastAPI endpoint with JWT auth

---

### Phase 7 — RAG + LangChain + LangGraph + Agents
**Status: ⬜ Upcoming**

> Most employable AI engineering skill right now

- Vector DBs: set up ChromaDB locally, embed sentences, query nearest neighbor
- Chunking: ~500 token chunks with overlap before embedding
- RAG step by step: ingest → chunk → embed → store → retrieve → generate
- LangChain chains: loaders, splitters, embeddings, retriever, LLM
- Conversational RAG: add memory for conversation history
- **LangGraph agents**: stateful agents with nodes, edges, conditional routing
- **Model Context Protocol (MCP)**: connect agents to external tools
- **LangSmith tracing**: trace full RAG pipeline, see exactly where retrieval fails
- **Redis cache**: cache embeddings to reduce API calls and latency
- **RAGAS evaluation**: measure faithfulness, answer relevancy, context precision

---

### Phase 8 — Deploy + CI/CD + Portfolio
**Status: ⬜ Upcoming**

- Docker: write a Dockerfile for FastAPI — understand every line
- Deploy to Render.com or Railway.app — free tier
- **GitHub Actions**: run tests on push, deploy on merge to main
- Environment variables: `.env` files, never hardcode API keys
- 3 pinned GitHub projects with real READMEs + demo links
- HuggingFace Spaces: publish live AI demos
- Kaggle: at least one public competition submission

---

### Phase 9 — System Design for AI *(Optional)*
**Status: ⬜ Upcoming**

> Not required for first junior role. Separates junior from mid-level candidates.

- Async task queues: Celery + Redis — offload slow LLM calls to background workers
- Horizontal scaling: multiple FastAPI instances behind a load balancer
- Caching strategies: what to cache, for how long, when to invalidate
- Redis-based rate limiting at scale
- Database design for AI apps: conversation history, embeddings, eval results

---

## 👨‍💻 Author

**Carl Joshua M. Coloma**
Computer Science — Software Engineering
AI Engineering Track

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/cdobby18)

---

*Last updated: May - 2026*