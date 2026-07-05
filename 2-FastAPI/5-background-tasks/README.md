# 5 · Background Tasks & Async Patterns

The most AI-relevant section in this phase. Model inference is slow, so this covers the four patterns for not blocking the HTTP response on it: load-once startup, fire-and-forget jobs, concurrent I/O, and token-by-token streaming.

---

## Progress Checklist

- [x] `main.py` — `lifespan` context manager loads a fake ML model once at startup (not per-request); `BackgroundTasks` fire-and-forget job pattern with a poll endpoint; async RAG pattern using `asyncio.gather` to fetch context and call an LLM concurrently; SSE token streaming via `StreamingResponse`

---

## The Four Patterns

| Pattern | Endpoint | Use when |
|---------|----------|----------|
| Sync | `POST /predict/sync` | Model is fast (<100ms) or you're just prototyping |
| Background job | `POST /predict/async` → `GET /jobs/{id}` | Slow inference — return a job ID immediately, client polls |
| Async concurrent I/O | `POST /predict/rag` | Multiple independent I/O calls (vector DB fetch + LLM call) that don't depend on each other |
| Streaming (SSE) | `POST /predict/stream` | Token-by-token UX — same mechanism ChatGPT/Claude.ai use |

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `@asynccontextmanager` + `lifespan=` | Load the model once at app startup, clean up on shutdown — never inside a request handler |
| `BackgroundTasks.add_task(fn, ...)` | Runs *after* the response is already sent to the client |
| `asyncio.gather(...)` | Run independent `await`-able calls concurrently instead of sequentially |
| `StreamingResponse(gen, media_type="text/event-stream")` | Streams a generator's output as Server-Sent Events |
| `data: <token>\n\n` ... `data: [DONE]\n\n` | The SSE wire format — client reads with `EventSource` or a `ReadableStream` |
| `GET /health` | Readiness probe — the pattern Kubernetes/load balancers poll before routing traffic to a pod |

---

## Gotcha

`predict_sync` calls `time.sleep(0.1)` inside a regular `def` route — that blocks FastAPI's whole worker thread, not just this request. `predict_with_rag` and `predict_stream` use `async def` with `await asyncio.sleep(...)`, which yields control back to the event loop so other requests keep being served. Mixing blocking calls into `async def` routes (e.g., calling a sync-only DB driver) reintroduces the same blocking problem — the `async` keyword alone doesn't make blocking code non-blocking.
