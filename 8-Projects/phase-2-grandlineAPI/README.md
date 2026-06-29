# Grand Line API

A production-pattern REST API built with FastAPI that tracks pirates, crews, and bounties across the Grand Line. This is Phase 2 of the AI Engineering roadmap, focusing on building the kind of backend that AI-powered APIs are built on.

---

## System Overview

**Tech Stack**

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (ASGI) |
| Auth | JWT via python-jose |
| Validation | Pydantic v2 |
| Rate Limiting | slowapi |
| Storage | In-memory (Python lists) |

**Project Structure**

```
phase-2-grandlineAPI/
├── main.py                    # App entry point — wires everything together
├── requirements.txt
└── app/
    ├── config.py              # App constants (secret key, credentials)
    ├── models.py              # TypedDict definitions (type hints for data)
    ├── store.py               # In-memory data store (crews_db, pirates_db)
    ├── auth/
    │   ├── jwt_handler.py     # Token creation and decoding
    │   └── jwt_bearer.py      # FastAPI dependency for protected routes
    ├── middleware/
    │   ├── logger.py          # Request/response logging middleware
    │   └── rate_limiter.py    # slowapi limiter instance
    ├── routes/
    │   ├── auth.py            # POST /auth/login
    │   ├── pirates.py         # Pirate CRUD endpoints
    │   └── crews.py           # Crew CRUD + nested /crews/{id}/pirates
    └── schemas/
        ├── pirate.py          # PirateCreate, PirateUpdate, PirateResponse
        └── crew.py            # CrewCreate, CrewUpdate, CrewResponse
```

---

## System Architecture

```
Client (curl / Swagger UI / Frontend)
          │
          ▼
  ┌───────────────────┐
  │  SlowAPIMiddleware │  ← Rate limiting (429 if exceeded)
  └────────┬──────────┘
           │
  ┌────────▼──────────┐
  │  log_requests      │  ← Logs [METHOD] /path → status (Xms)
  └────────┬──────────┘
           │
  ┌────────▼──────────────────────────────┐
  │  FastAPI Router                        │
  │  /auth  /pirates  /crews              │
  └────────┬──────────────────────────────┘
           │
  ┌────────▼──────────┐      ┌──────────────────┐
  │  Route Handler     │─────▶│  get_current_marine│  (protected routes only)
  └────────┬──────────┘      │  Depends(oauth2)  │
           │                 └──────────────────┘
  ┌────────▼──────────┐
  │  store.py          │  ← Read/write in-memory lists
  │  (pirates_db       │
  │   crews_db)        │
  └───────────────────┘
           │
  ┌────────▼──────────┐
  │  BackgroundTasks   │  ← Runs after response is sent (bounty recalc)
  └───────────────────┘
```

---

## Data Flow — Request Lifecycle

Every request flows through this chain:

1. **Client** sends HTTP request with optional `Authorization: Bearer <token>` header
2. **SlowAPIMiddleware** checks the IP's request count against limits; returns 429 if exceeded
3. **log_requests middleware** records the start time
4. **FastAPI router** matches the path and HTTP method to a handler function
5. **Dependency injection** runs `get_current_marine()` for protected routes — validates JWT, extracts username
6. **Route handler** runs: reads/writes `store.py` lists, builds response dict
7. **Pydantic response_model** validates and serializes the return value
8. **log_requests middleware** calculates duration and logs the result
9. **Client** receives the HTTP response
10. **BackgroundTasks** (if any) run after the response is sent

---

## Authentication Flow

```
1. Client → POST /auth/login
           body: username=marine&password=justice (form data)
           │
2. Server  → checks credentials against config.py constants
           → calls create_access_token({"sub": "marine"})
           → returns {"access_token": "<jwt>", "token_type": "bearer"}
           │
3. Client  → stores the token, sends it on future requests:
           Authorization: Bearer <jwt>
           │
4. Server  → get_current_marine() dependency decodes the JWT
           → extracts "sub" claim
           → if valid: route runs
           → if invalid/expired: 401 Unauthorized
```

Tokens expire after 30 minutes (configured in `config.py`).

---

## Rate Limiting

Rate limiting is implemented with [slowapi](https://github.com/laurentS/slowapi), which wraps the `limits` library and integrates natively with FastAPI.

**How it works:**
- `Limiter(key_func=get_remote_address)` — tracks limits per client IP
- Limits are applied as decorators directly on route functions
- When a limit is exceeded, slowapi returns `429 Too Many Requests` automatically

**Limits per route group:**

| Route | Limit | Reason |
|---|---|---|
| `POST /auth/login` | 10/minute | Prevent brute-force attacks |
| All GET routes | 60/minute | Normal read traffic |
| POST / PUT / DELETE | 30/minute | Write operations are more expensive |

**Example 429 response:**
```json
{
  "error": "Rate limit exceeded: 10 per 1 minute"
}
```

**Why this matters for AI APIs:** AI inference endpoints are expensive. A single LLM call can cost orders of magnitude more than a database read. Rate limiting is not optional — it protects your GPU budget and prevents abuse.

---

## Background Tasks

When a pirate is created via `POST /pirates`, the route adds a background task:

```
Client → POST /pirates → 201 response sent immediately
                      ↓
              recalculate_bounty(pirate_id) runs AFTER response
              bounty * 1.1 (10% increase applied)
```

This is the **fire-and-forget** pattern. The client doesn't wait for the background work — they get the 201 instantly. The server does the work afterward.

**Why this matters for AI APIs:** This is exactly how you'd handle AI inference at scale. The client gets a job ID immediately, the model runs in the background, and the result is stored when ready. You build on top of this pattern with task queues (Celery, ARQ) and webhooks.

---

## API Reference

**Base URL:** `http://localhost:8000`  
**Docs:** `http://localhost:8000/docs`

### Auth

| Method | Path | Auth | Body | Description |
|---|---|---|---|---|
| POST | `/auth/login` | No | form: username, password | Get JWT token |

### Pirates

| Method | Path | Auth | Body | Description |
|---|---|---|---|---|
| GET | `/pirates` | No | — | List all pirates |
| GET | `/pirates/{id}` | No | — | Get one pirate |
| POST | `/pirates` | Yes | PirateCreate | Create pirate |
| PUT | `/pirates/{id}` | Yes | PirateUpdate | Update pirate |
| DELETE | `/pirates/{id}` | Yes | — | Delete pirate |

### Crews

| Method | Path | Auth | Body | Description |
|---|---|---|---|---|
| GET | `/crews` | No | — | List all crews |
| GET | `/crews/{id}` | No | — | Get one crew |
| POST | `/crews` | Yes | CrewCreate | Create crew |
| PUT | `/crews/{id}` | Yes | CrewUpdate | Update crew |
| DELETE | `/crews/{id}` | Yes | — | Delete crew |
| GET | `/crews/{id}/pirates` | No | — | List pirates in crew |

---

## Running the Project

```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Open Swagger UI
open http://localhost:8000/docs
```

**Test the full flow:**

```bash
# 1. Login and capture token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -d "username=marine&password=justice" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. List crews (public)
curl http://localhost:8000/crews

# 3. Create a pirate (protected)
curl -X POST http://localhost:8000/pirates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Shanks", "bounty": 4048900000, "role": "Captain"}'

# 4. Check pirates in a crew
curl http://localhost:8000/crews/1/pirates
```

---

## FastAPI Concepts for AI Engineers

This section covers the FastAPI features you will use constantly when building AI-powered APIs. These aren't just web dev concepts — they map directly to the problems AI backends face.

---

### 1. Async / Await

FastAPI is built on ASGI (Asynchronous Server Gateway Interface). Every route can be `async def`, meaning the server handles multiple requests concurrently without blocking.

```python
@app.get("/inference")
async def run_inference(prompt: str):
    result = await call_llm(prompt)  # doesn't block other requests while waiting
    return {"result": result}
```

**Why it matters:** LLM inference takes 2–30 seconds. With sync handlers, your server can only handle one request at a time. With `async`, it handles hundreds concurrently while each one awaits its model response.

---

### 2. BackgroundTasks

Run work after the response is sent. The client doesn't wait.

```python
@app.post("/generate")
async def generate(prompt: str, background_tasks: BackgroundTasks):
    job_id = create_job(prompt)
    background_tasks.add_task(run_model, job_id, prompt)
    return {"job_id": job_id, "status": "queued"}
```

**Why it matters:** AI inference, embedding generation, and fine-tuning jobs are slow. The standard pattern is: create a job, return an ID immediately, run the work in the background, let the client poll for results.

---

### 3. Dependency Injection — `Depends()`

FastAPI's dependency system runs reusable logic before your route executes. Dependencies can be chained, cached, and tested independently.

```python
def get_model():
    return load_model("gpt2")  # loaded once, reused across requests

@app.post("/embed")
async def embed(text: str, model=Depends(get_model)):
    return {"embedding": model.encode(text)}
```

**Why it matters:** You use `Depends()` for: loading ML models at startup, validating API keys, injecting database sessions, enforcing rate limits per user tier. It keeps route handlers clean and makes testing easy — you can swap the dependency in tests.

---

### 4. Pydantic — Data Validation

Pydantic enforces types, constraints, and defaults on every request body and response. If the client sends bad data, FastAPI returns a 422 automatically — your handler never even runs.

```python
class InferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=4096)

@app.post("/generate", response_model=InferenceResponse)
async def generate(body: InferenceRequest):
    ...
```

**Why it matters:** AI APIs have strict input constraints (token limits, parameter ranges, required fields). Pydantic enforces these at the boundary — before your model ever sees the input. It also auto-generates the OpenAPI schema so clients know exactly what to send.

---

### 5. Middleware

Middleware intercepts every request before routing and every response before delivery.

```python
@app.middleware("http")
async def add_latency_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Inference-Time"] = f"{(time.perf_counter() - start):.3f}s"
    return response
```

**Use cases for AI APIs:**
- Log every prompt and response for audit/debugging
- Add CORS headers for browser clients
- Track token usage per request
- Reject requests that exceed prompt length before they hit the model

---

### 6. Streaming Responses — `StreamingResponse`

LLMs generate tokens one at a time. Streaming sends each token to the client as it's produced rather than waiting for the full response.

```python
from fastapi.responses import StreamingResponse

async def token_stream(prompt: str):
    async for token in llm.stream(prompt):
        yield f"data: {token}\n\n"  # Server-Sent Events format

@app.get("/stream")
async def stream(prompt: str):
    return StreamingResponse(token_stream(prompt), media_type="text/event-stream")
```

**Why it matters:** This is how ChatGPT's UI works. Users see tokens appear in real time instead of staring at a spinner for 10 seconds. You will implement this on every LLM-facing route in production.

---

### 7. File Uploads — `UploadFile`

Accept binary files (images, audio, PDFs) as multipart form data.

```python
from fastapi import UploadFile, File

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    content = await audio.read()
    transcript = await whisper_model.transcribe(content)
    return {"transcript": transcript}
```

**Why it matters:** Multimodal AI (vision, audio, document understanding) requires file inputs. `UploadFile` gives you async streaming reads so large files don't block the server.

---

### 8. WebSockets

Persistent bidirectional connection for real-time AI interactions.

```python
@app.websocket("/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for token in llm.stream(message):
            await websocket.send_text(token)
```

**Why it matters:** Conversational AI agents, live voice transcription, and interactive coding assistants require persistent connections. HTTP request-response is too slow for sub-second token delivery.

---

### 9. Rate Limiting

Protect expensive AI endpoints from overuse. Each model call costs money and compute.

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate")
@limiter.limit("5/minute")  # max 5 LLM calls per minute per IP
async def generate(request: Request, body: InferenceRequest):
    ...
```

**Strategies for AI APIs:**
- Rate limit by IP for public endpoints
- Rate limit by API key for authenticated endpoints
- Implement per-tier limits (free: 10/day, pro: 1000/day)
- Use Redis-backed limits for distributed deployments

---

### 10. OpenAPI / Swagger Auto-Docs

FastAPI generates interactive API documentation automatically from your type hints and Pydantic models. No manual docs needed.

- **Swagger UI** — `http://localhost:8000/docs` — interactive, lets you test endpoints
- **ReDoc** — `http://localhost:8000/redoc` — clean reference docs
- **OpenAPI JSON** — `http://localhost:8000/openapi.json` — machine-readable schema

```python
app = FastAPI(
    title="Inference API",
    description="LLM inference endpoints with streaming support",
    version="2.0.0",
)

@app.post("/generate", response_model=InferenceResponse, summary="Run text generation")
async def generate(body: InferenceRequest):
    """
    Send a prompt and receive a generated completion.
    Requires a valid API key in the Authorization header.
    """
```

**Why it matters:** Auto-docs let frontend teams and AI clients (like Claude) understand your API instantly. The OpenAPI schema can be imported into Postman, used to generate client SDKs, or fed to an AI agent as a tool definition.

---

### 11. CORS — Cross-Origin Resource Sharing

Browsers block requests from one domain to another unless the server explicitly allows it. Required when a web frontend calls your API.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Why it matters:** If you build a chat UI, an AI dashboard, or any browser-based frontend that calls your FastAPI backend, CORS must be configured or every browser request will be blocked with an error the user can't see.

---

### 12. Error Handling — `HTTPException` and Custom Handlers

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# Route-level: raise directly
raise HTTPException(status_code=404, detail="Resource not found")

# App-level: catch a specific exception type globally
@app.exception_handler(ModelTimeoutError)
async def model_timeout_handler(request: Request, exc: ModelTimeoutError):
    return JSONResponse(status_code=503, content={"error": "Model timed out", "retry_after": 5})
```

**Why it matters:** AI inference can fail in unique ways — model timeouts, out-of-memory errors, content policy violations, token limit exceeded. Custom exception handlers let you return consistent, structured error responses instead of 500s, and give clients enough information to retry intelligently.

---

## Key Takeaways

| Concept | Used In This Project | AI Engineering Application |
|---|---|---|
| Async/Await | All route handlers | Non-blocking LLM calls |
| BackgroundTasks | POST /pirates (bounty recalc) | Async inference jobs |
| Depends() | JWT auth on all writes | Model loading, API key validation |
| Pydantic | All request/response schemas | Prompt validation, structured output |
| Middleware | Logger, rate limiter | Token counting, CORS, audit logging |
| StreamingResponse | (Next project) | Real-time token streaming |
| Rate Limiting | All endpoints via slowapi | Protecting GPU-backed endpoints |
| OpenAPI Docs | Auto-generated at /docs | Self-documenting AI APIs |
