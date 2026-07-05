# Phase 2 · FastAPI

This phase takes you from a bare FastAPI app to the patterns you'll actually ship: validated request/response schemas, modular routers with middleware, two flavors of authentication, and the async/background-task patterns that keep an AI backend responsive while a model is thinking.

**Prerequisite:** Phase 1 (Foundations)
**Next:** Phase 3 (Machine Learning)

---

## Structure

| Folder | Topic | Priority |
|--------|-------|----------|
| `1-basics/` | App setup, GET/POST routes, path vs query params | Required |
| `2-routing-and-validation/` | Pydantic schemas, response models, status codes | Required |
| `3-advanced-routing/` | APIRouter, middleware, CORS, JSON persistence | Required |
| `4-authentication/` | HTTP Basic Auth + JWT token auth | Required |
| `5-background-tasks/` | Lifespan, BackgroundTasks, async I/O, SSE streaming | Required |

---

## What AI Engineers Actually Need Here

All five sections are required — this is the API layer every model you build in Phase 3+ eventually sits behind. Section 4 matters less for the *specific* auth scheme (Basic vs JWT) than for the *pattern* — dependency injection for auth checks. Section 5 is the highest-leverage section for AI work specifically: lifespan model loading, background jobs, and SSE streaming are exactly how you keep an LLM-backed API from blocking on a 10-second inference call.

---

## Master Progress Checklist

### 1 · Basics
- [x] `main.py` — FastAPI app instance, GET/POST/DELETE routes, path params vs query params, Swagger UI

### 2 · Routing & Validation
- [x] `main.py` — Pydantic `BaseModel` schemas, `Field()` constraints, `response_model`, `HTTPException`, proper status codes, partial updates

### 3 · Advanced Routing
- [x] `main.py` — mounts custom middleware + CORS, includes a modular router
- [x] `schemas.py` — Enum-backed Pydantic schemas
- [x] `storage.py` — JSON file persistence
- [x] `middleware/timer.py` — custom timing middleware
- [x] `routes/issues.py` — `APIRouter` with full CRUD

### 4 · Authentication
- [x] `4a-basic-auth/main.py` — HTTP Basic Auth, timing-safe password comparison, role-based dependency chaining
- [x] `4b-jwt-auth/main.py` — signup/login, password hashing, JWT-protected routes
- [x] `4b-jwt-auth/models.py` — user/post/token Pydantic schemas
- [x] `4b-jwt-auth/auth/jwt_handler.py` — token creation + decoding
- [x] `4b-jwt-auth/auth/jwt_bearer.py` — `HTTPBearer` dependency that validates tokens

### 5 · Background Tasks
- [x] `main.py` — lifespan model loading, `BackgroundTasks` job pattern, async concurrent I/O, SSE token streaming

---

## Learning Path

```
1-basics → 2-routing-and-validation → 3-advanced-routing → 4-authentication → 5-background-tasks
```

---

## Resources

| Resource | What | Format | Cost |
|----------|------|--------|------|
| FastAPI official docs (fastapi.tiangolo.com) | The best reference for this whole phase — tutorial is written in the same order as this folder | Docs | Free |
| Pydantic docs — Models | Field validation, `Config`, `EmailStr` | Docs | Free |
| jwt.io | Decode/inspect any JWT, understand header.payload.signature | Interactive | Free |
| Starlette docs — Middleware | How the ASGI middleware stack actually executes | Docs | Free |
| MDN — Server-Sent Events | The protocol behind `/predict/stream` | Docs | Free |

---

## Capstone Project

**[Grand Line API](../8-Projects/phase-2-grandlineAPI/)** — A World Government tracking system for pirates, crews, and bounties.

Applies every section of Phase 2 end-to-end: a `routes/` + `schemas/` package structure (advanced routing), JWT login via `auth/jwt_handler.py` + `auth/jwt_bearer.py` protecting write routes (authentication), `middleware/logger.py` + `slowapi` rate limiting (middleware), and a `BackgroundTasks` call that recalculates a pirate's bounty after the response is already sent (background tasks) — all on an in-memory store, no database required.
