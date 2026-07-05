# AI Engineering Roadmap

This repository documents my structured, project-driven journey toward becoming a
**Junior AI Engineer** — from Python foundations all the way to deploying production
RAG systems and AI agents.

**From Zero to AI Engineer — one built project at a time.**

---

## The Path

```
AI-Roadmap/
│
├── 1-Foundations/
│     ├── 1-python-basics       # Variables, loops, functions, data structures
│     ├── 2-oop                 # Classes, inheritance, magic methods
│     ├── 3-dsa                 # Basic structures, sorting, algorithms
│     ├── 4-database            # SQLite, CRUD, joins, aggregations, Python integration
│     ├── 5-http-apis           # requests library, handling HTTP responses
│     └── 6-advanced-python     # asyncio, modules and packages
│
├── 2-FastAPI/
│     ├── 1-basics              # First endpoints, JSON responses
│     ├── 2-routing-and-validation  # Pydantic models, path/query params
│     ├── 3-advanced-routing    # Middleware, APIRouter, schemas
│     ├── 4-authentication      # Basic auth + JWT auth
│     └── 5-background-tasks    # Async background jobs
│
├── 3-ML/
│     ├── 1-data-analysis       # NumPy, Pandas, EDA
│     ├── 2-classical-ml        # Supervised + unsupervised, scikit-learn
│     ├── 3-deep-learning       # Neural networks, CNNs from scratch
│     ├── 4-pytorch             # Tensors, nn.Module, training loop
│     ├── 5-model-evaluation    # Metrics, confusion matrix, cross-validation
│     └── 6-ml-tools            # HuggingFace pipeline, W&B, Gradio
│
├── 4-NLP/
│     ├── text-preprocessing    # Tokenization, text pipelines
│     ├── text-representation   # Word2Vec, TF-IDF, word embeddings
│     ├── nlp-applications      # Sentiment, NER, summarization, chatbot
│     ├── pre-trained-models    # BERT classification, GPT text gen, HF Hub
│     └── transformers          # Attention mechanism, BERT embeddings, architecture
│
├── 5-LLMs/                     # Prompt engineering, tool calling, observability
│
├── 6-RAG/                      # Vector DBs, LangChain, LangGraph, RAGAS eval
│
├── 7-Deploy/                   # Docker, CI/CD, HuggingFace Spaces
│
├── 9-Notes/                    # Phase summary notes and quick reference
│
└── 8-Projects/
      ├── phase-1-devilfruit    # OOP + SQLite project (One Piece theme)
      └── phase-2-grandline-api # FastAPI project
```

---

## Progress

| Phase | Topic | Status |
|-------|-------|--------|
| 1 | Python Foundations + DSA + SQL | ✅ Complete |
| 2 | FastAPI + Auth + Background Tasks | 🔄 In Progress |
| 3 | Machine Learning + PyTorch + W&B | 🔄 In Progress |
| 4 | NLP + Transformers + Pre-trained Models | 🔄 In Progress |
| 5 | LLMs + Prompt Engineering + Observability | ⬜ Upcoming |
| 6 | RAG + LangChain + LangGraph + Agents | ⬜ Upcoming |
| 7 | Deploy + CI/CD + Portfolio | ⬜ Upcoming |
| 8 | Projects | 🔄 In Progress |

---

## Phase Breakdown

### Phase 1 — Python Foundations + DSA + SQL
**Status: ✅ Complete**

- Python basics: variables, operators, conditionals, loops, functions
- Data structures: lists, tuples, sets, dictionaries
- OOP: classes, `__init__`, `self`, inheritance, magic methods
- DSA: basic data structures, sorting algorithms, algorithmic thinking
- SQL: `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, aggregations, indexing using SQLite
- HTTP APIs: `requests` library, handling responses, real API calls
- Advanced Python: `asyncio`, modules, packages, `__init__.py`

---

### Phase 2 — FastAPI + Auth + Background Tasks
**Status: 🔄 In Progress**

> FastAPI chosen for its async support, automatic Swagger docs, and native Pydantic integration — critical for production AI backends.

- GET and POST endpoints returning JSON
- Pydantic models for request/response validation
- Async endpoints: `async/await` and why it matters for AI workloads
- Path params, query params, request bodies
- Middleware and APIRouter for clean project structure
- Basic auth and **JWT authentication** — protect endpoints with `python-jose` + `passlib`
- Background tasks: fire-and-forget async jobs

---

### Phase 3 — Machine Learning + PyTorch + Experiment Tracking
**Status: 🔄 In Progress**

- NumPy + Pandas: vectorized operations, DataFrames, EDA
- Classical ML: supervised (linear, tree-based) and unsupervised models with scikit-learn
- Deep learning: build neural networks and CNNs from scratch — understand every layer
- PyTorch: tensors, autograd, `nn.Module`, full training loop (forward, loss, backward, optimizer)
- Model evaluation: confusion matrix, precision/recall, cross-validation — never evaluate on training data
- HuggingFace `pipeline()` for inference in 5 lines
- **W&B experiment tracking** — log accuracy, loss, hyperparameters from day 1
- Gradio: wrap any model in a demo UI, publish to HuggingFace Spaces

---

### Phase 4 — NLP + Transformers + Pre-trained Models
**Status: 🔄 In Progress**

- Tokenization: LLMs read tokens, not words — inspect tokenizer output directly
- Word embeddings: Word2Vec — a word as a list of numbers encoding meaning
- TF-IDF: implement from scratch, understand when to use vs dense embeddings
- NLP tasks: sentiment analysis, NER, summarization via HuggingFace
- Transformer architecture: attention mechanism, self-attention (Q/K/V), multi-head attention
- Positional encoding: how transformers encode order without recurrence
- BERT (encoder-only) vs GPT (decoder-only) — hands-on with both
- Fine-tuning: HuggingFace `Trainer` on a custom dataset, push to Hub

---

### Phase 5 — LLMs + Prompt Engineering + Observability
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

### Phase 6 — RAG + LangChain + LangGraph + Agents
**Status: ⬜ Upcoming**

> Most employable AI engineering skill right now

- Vector DBs: ChromaDB locally, embed sentences, query nearest neighbor
- Chunking: ~500 token chunks with overlap before embedding
- RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- LangChain chains: loaders, splitters, embeddings, retriever, LLM
- Conversational RAG: add memory for multi-turn history
- **LangGraph agents**: stateful agents with nodes, edges, conditional routing
- **Model Context Protocol (MCP)**: connect agents to external tools
- **LangSmith tracing**: trace full RAG pipeline, see exactly where retrieval fails
- **Redis cache**: cache embeddings to reduce API calls and latency
- **RAGAS evaluation**: measure faithfulness, answer relevancy, context precision

---

### Phase 7 — Deploy + CI/CD + Portfolio
**Status: ⬜ Upcoming**

- Docker: write a Dockerfile for FastAPI — understand every line
- Deploy to Render.com or Railway.app — free tier
- **GitHub Actions**: run tests on push, deploy on merge to main
- Environment variables: `.env` files, never hardcode API keys
- 3 pinned GitHub projects with real READMEs + demo links
- HuggingFace Spaces: publish live AI demos
- Kaggle: at least one public competition submission

---

### Phase 8 — Projects
**Status: 🔄 In Progress**

| Project | Phase | Description |
|---------|-------|-------------|
| [Devil Fruit Database](8-Projects/phase-1-devilfruit/) | 1 | OOP + SQLite CLI — One Piece themed |
| [Grand Line API](8-Projects/phase-2-grandline-api/) | 2 | FastAPI REST API project |

---

## Author

**Carl Joshua M. Coloma**
Computer Science — Software Engineering
AI Engineering Track

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/cdobby18)

---

*Last updated: June 2026*
