# Phase 5 — LLMs + Prompt Engineering + Observability

**Status: ⬜ Upcoming**

Working with large language models as an engineer, not just a user.

## What this phase will cover

- Tokens, context window, temperature — the parameters that actually matter
- Zero-shot, few-shot, chain-of-thought prompting — implement and compare all three
- System prompts: shaping model behavior across all turns
- Function/tool calling: the LLM decides when to call your Python function
- Structured outputs: force valid JSON using native API support
- **LangSmith / Langfuse** — trace every LLM call: latency, token usage, errors
- **Prompt injection** — understand the attack, implement input sanitization
- Ollama: run models locally (llama3, mistral) — reduce API costs while learning
- Serve a chatbot as a proper async FastAPI endpoint with JWT auth

## Builds on

- Phase 2 (FastAPI, JWT auth) — the serving layer for LLM endpoints
- Phase 4 (transformers, tokenization) — what's actually happening inside the model
