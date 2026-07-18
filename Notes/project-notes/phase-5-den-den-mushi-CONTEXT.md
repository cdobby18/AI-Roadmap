# Den Den Mushi — Context

**Phase:** 5 — LLMs + Prompt Engineering + Observability
**Theme:** An LLM communications hub — route queries across providers, equip with tools, enforce structured outputs, track everything, and stay secure.

---

## What This Builds

A single gateway that takes a user query and:
1. **Routes** it to the best provider (OpenAI, Anthropic, or local Ollama)
2. **Equips** the LLM with tools (calculator, web search, weather)
3. **Enforces** structured JSON outputs validated against schemas
4. **Tracks** every call — latency, tokens, cost, errors
5. **Protects** against prompt injection and abuse
6. **Remembers** conversation context across turns
7. **Evaluates** itself against a benchmark suite

This is what a production LLM application looks like — not a single script, but a layered system where every concern has its own module.

---

## What It Covers

| Topic | Where |
|-------|-------|
| Multi-provider routing | `router.py` — cost/speed-based dispatch |
| Tool calling | `tools.py` — discoverable tool registry |
| Structured outputs | `structured_output.py` — Pydantic validation |
| Context management | `memory.py` — sliding window + token budgeting |
| Observability | `observability.py` — logs, latency, cost tracking |
| Security | `security.py` — injection detection, rate limits |
| Reasoning patterns | `reasoning.py` — CoT, reflection loop |
| Evaluation | `evaluate.py` — benchmark against test set |
| Deployment | `app.py` — CLI + FastAPI, Docker-ready |

---

## How to Run

```bash
pip install -r requirements.txt

# CLI mode
python app.py ask "What is the weather in Tokyo?" --tool-use

# Interactive chat
python app.py chat

# FastAPI
uvicorn app:fastapi_app --reload
# POST /ask  {"query": "hello", "provider": "auto"}

# Benchmark
python evaluate.py --queries test_set.json
```

---

## Files

| File | What It Does |
|------|-------------|
| `config.py` | Provider settings, API keys from env, rate limits |
| `providers.py` | Unified interface over OpenAI, Anthropic, Ollama |
| `router.py` | Routes queries by cost, speed, availability |
| `tools.py` | Tool registry — define, discover, dispatch |
| `structured_output.py` | JSON schema enforcement via Pydantic |
| `memory.py` | Conversation history with token budgeting |
| `observability.py` | Call logging, latency P50/P95, cost tracking |
| `security.py` | Prompt injection detection, input validation |
| `reasoning.py` | Chain-of-thought, reflection, self-critique |
| `evaluate.py` | Benchmark runner with scored test cases |
| `app.py` | CLI entry point + FastAPI application |
