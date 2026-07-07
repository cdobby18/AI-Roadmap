# Grand Line API — Lessons

**Phase:** 2 — FastAPI + Auth + Background Tasks

Every FastAPI feature below is exercised in this project, and each one maps directly onto a problem AI-serving backends face — that mapping is the actual point of Phase 2, not just "learn a web framework."

---

## 1. Async / Await

`async def` route handlers let Uvicorn serve many requests concurrently without blocking. LLM inference takes 2–30 seconds; with sync handlers the server handles one request at a time, with `async` it handles hundreds concurrently while each awaits its model response.

## 2. BackgroundTasks

`background_tasks.add_task(...)` runs work *after* the response is sent (used here for bounty recalculation). This is the standard pattern for slow AI work: create a job, return an ID immediately, run inference in the background, let the client poll for the result.

## 3. Dependency Injection — `Depends()`

`get_current_marine()` runs before protected routes and validates the JWT. The same mechanism is how you'd load an ML model once at startup and hand it to every route (`Depends(get_model)`), validate API keys, or inject a DB session — and it's independently testable/swappable.

## 4. Pydantic Validation

Every request/response has a schema (`schemas/pirate.py`, `schemas/crew.py`). Bad input never reaches the handler — FastAPI returns 422 automatically. AI APIs need exactly this at the boundary: token limits, temperature ranges, required fields, all enforced before the model ever sees the input.

## 5. Middleware

`logger.py` wraps every request/response. In an AI API the same slot is where you'd log every prompt/response for audit, track token usage per request, or reject over-length prompts before they hit the model.

## 6. Rate Limiting (`slowapi`)

Applied per-route via `@limiter.limit(...)`, keyed by IP. AI inference is expensive per call — rate limiting isn't optional, it protects compute budget. Production versions of this add per-API-key tiers and Redis-backed limits for distributed deployments.

## 7. JWT Auth End-to-End

Login → token → `Authorization: Bearer` → dependency decodes and validates → route runs or 401. This exact flow is what gates any real API, AI-serving or not.

## 8. OpenAPI / Swagger Auto-Docs

Generated from type hints and Pydantic models with zero manual docs (`/docs`, `/redoc`, `/openapi.json`). The schema is also machine-readable enough to be imported into Postman or handed to an agent as a tool definition.

---

## Not Built Here, But the Natural Next Step

- **Streaming responses** (`StreamingResponse` / SSE) — how ChatGPT-style token-by-token output works; not needed here because responses are just JSON dicts, but the natural addition once an LLM-backed route exists.
- **WebSockets** — persistent bidirectional connection for conversational agents or live transcription.
- **File uploads** (`UploadFile`) — needed once a route accepts images/audio/PDFs (multimodal input).
- **CORS** — required the moment a browser frontend calls this API directly.

---

## Key Takeaways

| Concept | Used In This Project | AI Engineering Application |
|---|---|---|
| Async/Await | All route handlers | Non-blocking LLM calls |
| BackgroundTasks | `POST /pirates` bounty recalc | Async inference jobs |
| `Depends()` | JWT auth on all writes | Model loading, API key validation |
| Pydantic | All request/response schemas | Prompt validation, structured output |
| Middleware | Logger, rate limiter | Token counting, CORS, audit logging |
| Rate limiting | `slowapi` on every route | Protecting GPU-backed endpoints |
| OpenAPI docs | Auto-generated at `/docs` | Self-documenting AI APIs |

---

## Where This Sits in the Roadmap

Phase 1 taught raw CRUD against a real database (`phase-1-devilfruit`); this project swaps that for the web-framework layer on top — same CRUD shape, now behind HTTP, auth, and validation. The in-memory `store.py` is a deliberate stand-in for what would be a database in production.

**Forward reference:** Phase 3's `BountyNet` model (`phase-3-bountyhunter/model.py`) is built to be served exactly through this pattern — load the checkpoint once via `Depends()`, accept input through a Pydantic schema, return the prediction as JSON. Everything learned here about `Depends()`, Pydantic, and background tasks is what makes that possible without re-learning FastAPI from scratch.
