# Den Den Mushi — Lessons

**Phase:** 5 — LLMs + Prompt Engineering + Observability

---

## What This Project Teaches

### 1. Providers are interchangeable — if you abstract them properly
The `BaseProvider` ABC + separate implementations for OpenAI, Anthropic, and Ollama means you can swap providers without changing a single line of application logic. The hard part isn't calling the API — it's normalizing the response format, token counts, and error handling across providers that all speak different dialects.

### 2. Routing is a business decision, not a technical one
The `router.py` module encodes strategy: cheap/simple queries go to Ollama (free), complex/tool-heavy queries go to OpenAI. In production, routing decisions involve cost tracking, latency SLAs, fallback chains, and A/B testing — the module structure makes this explicit.

### 3. Tools need a registry, not if/else chains
The `tools.py` module registers tools declaratively with JSON schemas. Adding a new tool is `register_tool(ToolSpec(...))` — no changes to dispatch logic, no new if/else branches. This is the pattern LangChain uses, and building it from scratch makes you appreciate why.

### 4. Structured outputs are a contract, not a suggestion
Without Pydantic validation, the LLM can return malformed JSON and your app silently breaks. The `structured_output.py` module validates against schemas and surfaces errors cleanly — this is the same pattern used by instructor, Outlines, and jsonformer libraries.

### 5. Observability must be baked in, not bolted on
The `Logger` class records every call automatically. Without this, you have no idea which provider is costing you money, which queries are slow, or where errors come from. The `CallRecord` dataclass captures everything needed to debug a production incident.

### 6. Security is layered
Input validation → injection detection → rate limiting. Each layer is independent and testable. The `security.py` module shows that prompt injection defense isn't perfect (regexes can be bypassed) but layered defense-in-depth is better than nothing.

### 7. Evaluation prevents regressions
The `evaluate.py` benchmark runner scores responses against keyword coverage and length thresholds. As you tweak prompts or swap models, the benchmark tells you if quality improved or degraded. Without this, you're flying blind.

---

## Phase 5 Skills Demonstrated

- [x] Multi-provider abstraction (OpenAI, Anthropic, Ollama)
- [x] Tool calling with JSON schema definitions
- [x] Structured output enforcement with Pydantic
- [x] Context management with token budgeting
- [x] Observability — per-call logging, latency, cost tracking
- [x] Security — prompt injection detection, rate limiting
- [x] Reasoning patterns — chain-of-thought, reflection
- [x] Evaluation — benchmark runner with scored test cases
- [x] Dual entry points — CLI + FastAPI
- [x] Configuration from environment variables

---

## Forward Reference — Phase 7 (LangGraph)

The routing + tool dispatch in this project is a **graph** in disguise:

```
input → [validate] → [detect injection] → [route to provider] → [tool? yes→dispatch→route again] → [log] → output
```

In LangGraph, each of these steps becomes a **node**, and the edges become conditional branches. The `router.py` decision logic becomes a `Route` condition. The tool dispatch becomes a `ToolNode`. The logging becomes a global callback.

This project is the hand-written version of what LangGraph automates. Understanding the manual version first makes the graph version obvious.
