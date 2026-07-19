# Phase 2 — FastAPI

## What FastAPI Is

A Python web framework for building APIs. It's the industry standard for serving ML models because:
- **Automatic OpenAPI docs** — `/docs` endpoint is free documentation.
- **Pydantic validation** — payloads validated at the boundary before your handler runs.
- **Async support** — but sync routes run in a threadpool, so you don't need async for blocking work like model inference.
- **Dependency injection** — shared logic (auth, DB sessions) without global state or tight coupling.

## Why FastAPI over Flask or Django

| Framework | Best for |
|-----------|----------|
| FastAPI | ML/AI backends, microservices, async I/O |
| Flask | Simple APIs, prototyping, small projects |
| Django | Full-stack apps with ORM, admin, auth built-in |

FastAPI wins for AI because: automatic docs (stakeholders can test endpoints immediately), native async (useful for concurrent API calls to LLMs/DBs), and Pydantic (catches bad inputs before they reach your model).

## Key Concepts

**Endpoints:** One URL, one job. GET for reading, POST for creating, PUT for updating, DELETE for removing. Pick the right HTTP method — it documents intent.

**Path vs query params:** `/items/5` (path, required) vs `/items?category=books` (query, optional/filtering). FastAPI extracts both from type hints.

**Pydantic schemas:** Define `BaseModel` subclasses for request/response shapes. Validation errors (422) are automatic. Use `response_model` on routes to filter/transform output — never return raw DB models.

**Dependency injection (Depends):** Functions that run before the handler. Use for: auth checks, DB sessions, pagination, rate limit checks, config loading. FastAPI caches dependencies per request.

**Middleware:** Code that runs on every request/response — logging, timing, CORS headers, security. `BaseHTTPMiddleware` for custom middleware; `CORSMiddleware` is built-in.

**BackgroundTasks:** Lightweight deferred work (logging, email, cache refresh). Runs in the same process — NOT for heavy CPU work. Heavy work belongs in a task queue (Celery, ARQ).

**JWT auth pattern:** Client sends `Authorization: Bearer <token>`. Server decodes with a secret key, extracts user identity from the payload. Stateless — no server-side session storage. Downside: hard to revoke early (tokens live until expiry). Use short expiry + refresh tokens.

**CORS:** Browser security. If your frontend is on a different origin than your API, you must configure CORS to allow it. Not an issue for server-to-server calls — only browsers enforce it.

**Rate limiting:** Cap requests per client per time window. Use `slowapi` for FastAPI. Essential for public inference endpoints to control cost and prevent abuse.

## Production Considerations

- **Environment variables** — never hardcode secrets. Use `pydantic-settings` or `python-decouple`.
- **Logging** — use `structlog` or at minimum `logging` with structured output. Log request IDs, latency, errors.
- **Health checks** — `/health` endpoint for load balancers / Docker healthchecks.
- **Graceful shutdown** — close DB connections, flush metrics on SIGTERM.
- **CPU-bound work in sync `def`** — FastAPI runs sync routes in a threadpool automatically. Async routes (`async def`) block the event loop if they do CPU work.

## Interview Must-Knows

- Why FastAPI over Flask: automatic docs, Pydantic validation at the boundary, dependency injection, native async.
- How dependency injection works: FastAPI inspects type hints, builds the dependency tree, and caches per request.
- JWT vs sessions: JWT is stateless (scales across servers, hard to revoke). Sessions are stateful (stored server-side, easy to revoke, need sticky sessions or shared store).
- BackgroundTasks vs Celery: BackgroundTasks for light I/O in the same process; Celery for heavy work across multiple workers/processes.
- Status codes: 200 (success), 201 (created), 400 (client error), 401 (not authenticated), 403 (not authorized), 404 (not found), 422 (validation), 429 (rate limited), 500 (server error).
- Testing: `TestClient` for in-process tests without a running server. Mock external calls and DB.

## Common Pitfalls

- CPU work in `async def` — blocks the event loop. Use `def` for CPU/GPU-bound work.
- Returning raw DB models — leaks internal fields. Use `response_model` with a Pydantic schema.
- Forgetting CORS — works in curl/Postman, fails in browser. Always configure CORS for web frontends.
- Hardcoded secrets — store API keys, JWT secrets in environment variables.
- No rate limiting on public endpoints — unlimited inference calls can cost thousands.
- Not validating input beyond Pydantic — add business logic validation (e.g., "this user can only query their own data").
