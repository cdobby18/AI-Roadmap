# 🤖 AI Engineering Roadmap
### Carl Joshua M. Coloma — Computer Science, Software Engineering Track

<p align="center">
  <img src="image1.JPG" width="600"/><br><br>
  <img src="image2.JPG" width="600"/><br>
  <em>AI Engineering Roadmap Overview</em>
</p>

---

> *"The fastest way to learn is to build something you actually care about."*

This repository documents my structured, project-driven journey toward becoming a **Junior AI Engineer** — from Python foundations all the way to deploying production RAG systems and AI agents.

**Not a collection of tutorials. A record of things actually built.**

---

## 🧭 The Path

```
Python Foundations + SQL
        ↓
FastAPI + Auth + Security
        ↓
Machine Learning + Experiment Tracking (W&B)
        ↓
NLP Fundamentals
        ↓
Transformers — How They Actually Work
        ↓
LLMs + Prompt Engineering + Observability
        ↓
RAG + LangChain + LangGraph + Agents
        ↓
Deploy + CI/CD + Portfolio
```

**9 phases · ~37 weeks · Almost entirely free resources · Every phase ships a project**

---

## 🚀 Projects

| Project | Phase | Stack | Status |
|---------|-------|-------|--------|
| TextCleaner | Phase 1 | Python, OOP, File I/O | ⏳ Upcoming |
| FastAPI Text Processing API | Phase 2 | FastAPI, JWT, Pydantic, slowapi | ⏳ Upcoming |
| PH News Sentiment Classifier | Phase 3 | PyTorch, scikit-learn, W&B, Gradio | ⏳ Upcoming |
| Fine-tuned BERT on Local Dataset | Phase 4 | HuggingFace Trainer, W&B | ⏳ Upcoming |
| Transformer Explainer (Blog/README) | Phase 5 | Writing, Architecture Diagrams | ⏳ Upcoming |
| FastAPI Chatbot with Observability | Phase 6 | FastAPI, Anthropic API, LangSmith | ⏳ Upcoming |
| RAG Chatbot over PH Documents | Phase 7 | LangChain, LangGraph, ChromaDB, FastAPI, RAGAS | ⏳ Upcoming |
| Capstone — Live RAG App + CI/CD | Phase 8 | Docker, GitHub Actions, Render | ⏳ Upcoming |

> As each project is completed, this table will be updated with live demo links and GitHub links.

---

## 📊 Progress

| Phase | Topic | Status |
|-------|-------|--------|
| 1 | Python Foundations + SQL | 🔄 In Progress |
| 2 | FastAPI + Security Basics | ⏳ Upcoming |
| 3 | Machine Learning + W&B Tracking | ⏳ Upcoming |
| 4 | NLP Fundamentals | ⏳ Upcoming |
| 5 | Transformers — Architecture | ⏳ Upcoming |
| 6 | LLMs + Prompt Engineering + Observability | ⏳ Upcoming |
| 7 | RAG + LangChain + LangGraph + Agents | ⏳ Upcoming |
| 8 | Deploy + CI/CD + Portfolio | ⏳ Upcoming |
| 9 | System Design for AI *(optional)* | ⏳ Upcoming |

---

## 🧠 Phase Breakdown

### 🟢 Phase 1 — Python Foundations + SQL
**Status: 🔄 In Progress**

- OOP: classes, `__init__`, `self`, inheritance, magic methods
- Exceptions: `try/except/finally` — handle errors, not just print them
- File I/O: read/write text, CSV, JSON
- API requests: `requests` library, handle responses
- Modules and packages: `__init__.py`, importing your own code
- SQL basics: `SELECT`, `WHERE`, `JOIN`, `GROUP BY` using SQLite *(3-day module)*

**Milestone project:** `TextCleaner` — OOP + string processing + file I/O

---

### 🟦 Phase 2 — FastAPI + Security Basics
**Status: ⏳ Upcoming**

- Why FastAPI: async support, automatic docs, Pydantic validation
- GET and POST endpoints returning JSON
- Pydantic models for request validation — critical for AI APIs
- Async endpoints: `async/await` and why it matters
- Path params, query params, request bodies
- **JWT authentication** — protect endpoints with `python-jose` + `passlib`
- **Rate limiting** — `slowapi`, 10 requests/minute per user
- Environment variables: `Pydantic Settings` + `.env` files

**Milestone project:** FastAPI text processing API with JWT auth + rate limiting

---

### 🟡 Phase 3 — Machine Learning + Experiment Tracking
**Status: ⏳ Upcoming**

> NumPy and Pandas are learned here in context — not as a separate phase

- scikit-learn: train/test split, cross-validation, pipelines, metrics
- PyTorch: tensors, autograd, training loop — forward pass, loss, backward, optimizer
- `nn.Module` — build and understand every line of a neural network
- HuggingFace `pipeline()` for inference in 5 lines
- Evaluate properly: confusion matrix, never evaluate on training data
- **W&B experiment tracking** — log accuracy, loss, hyperparameters from day 1
- Gradio: wrap model in a demo UI, publish to HuggingFace Spaces

**Milestone project:** Philippine news sentiment classifier with W&B tracking + Gradio demo

---

### 🟣 Phase 4 — NLP Fundamentals
**Status: ⏳ Upcoming**

- Tokenization: LLMs read tokens, not words — inspect tokenizer output
- Word embeddings: Word2Vec — a word as a list of numbers encoding meaning
- TF-IDF: implement from scratch, understand when to use vs embeddings
- NLP tasks: sentiment analysis, NER, summarization via HuggingFace
- Fine-tuning: HuggingFace `Trainer` on a custom dataset
- Encoder (BERT) vs decoder (GPT) — conceptual understanding before Phase 5

**Milestone project:** Fine-tune BERT on a local Filipino/Philippine dataset

---

### 🔵 Phase 5 — Transformers: How They Actually Work
**Status: ⏳ Upcoming**

> Dedicated phase added based on mentor recommendation — before LLMs, understand the architecture

- Attention mechanism: every token attends to every other token simultaneously
- Self-attention: queries, keys, values — what they are and why the math works
- Multi-head attention: running attention in parallel
- Positional encoding: how transformers encode order without recurrence
- Encoder-only (BERT) vs decoder-only (GPT)
- Read *Attention Is All You Need* — abstract + architecture section minimum

**Milestone project:** Write a detailed README/blog post explaining transformers in your own words, with a diagram you drew yourself

---

### 🔴 Phase 6 — LLMs + Prompt Engineering + Observability
**Status: ⏳ Upcoming**

- Tokens, context window, temperature — know these cold
- Zero-shot, few-shot, chain-of-thought prompting — implement and compare all three
- System prompts: shape model behavior across all turns
- Function/tool calling: the LLM decides when to call your Python function
- Structured outputs: force valid JSON using native API support
- **LangSmith / Langfuse** — trace every LLM call: latency, token usage, errors
- **Prompt injection** — understand the attack, implement input sanitization
- Ollama: run models locally (llama3, mistral) — reduce API costs while learning
- Serve chatbot as a proper async FastAPI endpoint with JWT auth

**Milestone project:** FastAPI chatbot with memory, streaming, observability, and structured output

---

### ⚫ Phase 7 — RAG + LangChain + LangGraph + Agents
**Status: ⏳ Upcoming**

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

**Milestone project:** RAG chatbot over Philippine documents — LangChain + LangGraph + FastAPI + JWT + LangSmith + RAGAS eval report

---

### 🟤 Phase 8 — Deploy + CI/CD + Portfolio
**Status: ⏳ Upcoming**

- Docker: write a Dockerfile for FastAPI — understand every line
- Deploy to Render.com or Railway.app — free tier
- **GitHub Actions**: run tests on push, deploy on merge to main
- Environment variables: `.env` files, never hardcode API keys
- 3 pinned GitHub projects with real READMEs + demo links
- HuggingFace Spaces: publish live AI demos
- Kaggle: at least one public competition submission

**Milestone project:** Capstone — live RAG chatbot with CI/CD pipeline + HuggingFace Space demo

---

### 🔘 Phase 9 — System Design for AI *(Optional)*
**Status: ⏳ Upcoming**

> Not required for first junior role. Separates junior from mid-level candidates.

- Async task queues: Celery + Redis — offload slow LLM calls to background workers
- Horizontal scaling: multiple FastAPI instances behind a load balancer
- Caching strategies: what to cache, for how long, when to invalidate
- Redis-based rate limiting at scale
- Database design for AI apps: conversation history, embeddings, eval results

**Milestone project:** Architecture diagram — RAG chatbot handling 1,000 concurrent users

---

## 🧰 Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Backend / API | FastAPI |
| Auth & Security | JWT, python-jose, passlib, slowapi |
| ML Framework | scikit-learn, PyTorch |
| NLP / LLMs | HuggingFace Transformers, LangChain, LangGraph |
| Experiment Tracking | Weights & Biases (W&B) |
| Observability | LangSmith, Langfuse |
| Vector DB | ChromaDB, FAISS |
| Caching | Redis |
| LLM APIs | Anthropic (Claude), OpenAI, Ollama (local) |
| Evaluation | RAGAS |
| Deployment | Docker, Render, Railway, GitHub Actions |
| Portfolio | GitHub, HuggingFace Spaces, Kaggle |

---

## 👨‍💻 Author

**Carl Joshua M. Coloma**
Computer Science — Software Engineering
AI Engineering Track

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/cdobby18)

---

*Last updated: May 2026*