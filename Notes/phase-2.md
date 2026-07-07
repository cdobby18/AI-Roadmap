# Phase 2 — FastAPI

## Goal
Learn how to build an API backend that can serve AI or ML features in production, not just a demo script — routing, validation, auth, background work, and enough testing/design sense to defend your choices in an interview.

## What I need to know
- FastAPI app structure
- GET/POST routes and path/query params
- Pydantic models for input validation
- Dependency injection with `Depends`
- Middleware and request lifecycle
- Basic Auth and JWT auth patterns
- Background tasks for non-blocking work
- REST API design basics: status codes, versioning, idempotency
- Testing endpoints with `TestClient`
- Rate limiting and CORS

## Key terms
- `endpoint`: a route exposed by the API. One URL that performs one job, like returning predictions or saving user input.
- `Pydantic`: the library that checks the shape of incoming/outgoing JSON. Prevents bad inputs from reaching your logic.
- `BaseModel`: the Pydantic class used to define input/output schemas — how you declare what data the API expects and returns.
- `Depends`: FastAPI's dependency injection helper. Use it to reuse logic like authentication, database connections, or configuration across routes.
- `BackgroundTasks`: lets the server start a response immediately and run follow-up work later. Useful for email sending, logging, or cache refresh.
- `JWT`: JSON Web Token. A compact, signed string proving a user is authenticated without storing session state on the server. Has three parts: header, payload, signature.
- `bearer token`: an auth scheme where the client sends `Authorization: Bearer <token>` on every request; FastAPI reads it via a security dependency (e.g. `HTTPBearer`).
- `HTTPException`: stops the request and returns an error code. Use it for invalid data, unauthorized access, or missing resources.
- `middleware`: code that runs before or after every request — logging, timing, security headers, CORS.
- `CORS`: Cross-Origin Resource Sharing. Browser security rule that blocks a frontend on one origin from calling an API on another unless the API explicitly allows it.
- `rate limiting`: capping how many requests a client can make in a time window, to protect the service from abuse or overload (e.g. `slowapi`).
- `idempotency`: calling the same request multiple times produces the same result. `GET`, `PUT`, `DELETE` should be idempotent; `POST` typically is not.
- `status code`: `2xx` success, `4xx` client error (bad input, unauthorized), `5xx` server error. Interviewers expect you to pick the right one, not always `200`.

## When to use
- Use FastAPI when you need a web service for model inference or any AI feature behind an API.
- Use Pydantic whenever the API accepts or returns JSON — validate at the boundary, trust it inside.
- Use dependencies for shared logic like authentication, DB sessions, or pagination params.
- Use JWT for stateless auth across services; use sessions/cookies when you control a single server and want easy revocation.
- Use background tasks for lightweight I/O/deferred work — not for heavy CPU work (that belongs in a task queue like Celery).
- Use rate limiting on public or expensive endpoints (e.g. inference calls) to control cost and abuse.
- Use API versioning (`/v1/...`) when a breaking change is coming but old clients still need to work.

## Interview review
- Explain that FastAPI is popular because it generates OpenAPI docs automatically and validates payloads before your endpoint code runs, using type hints.
- If asked about `Depends`, say it's useful for injecting shared services without tight coupling, and that FastAPI resolves and caches dependencies per request.
- When talking about auth, describe the difference between cookie sessions (stateful, easy revoke, same-origin friendly) and stateless JWT (scales across services, harder to revoke early).
- Mention that background tasks are not for heavy CPU work; they run in the same process and can still block the event loop if not careful — heavy work goes in a real queue/worker.
- If asked how you'd test an API, mention `TestClient` for fast in-process tests without a running server, and mocking external calls/DB in unit tests.
- If asked about scaling reads, mention caching (Redis), pagination, and rate limiting before "just add more servers."
- Be ready to explain why you picked a status code: `400` for bad input, `401` for missing/invalid auth, `403` for authenticated but not allowed, `404` for missing resource, `422` for validation errors (FastAPI's default for bad Pydantic input).

## Common pitfalls
- Doing CPU-heavy work inside an `async def` route — it blocks the event loop for every other request. Use a regular `def` (FastAPI runs it in a thread pool) or offload to a worker.
- Returning raw DB models instead of a `response_model` — leaks internal fields and couples your API to your schema.
- Forgetting CORS config and being confused why the browser blocks a working curl request.
- Storing secrets (JWT signing keys, API keys) directly in code instead of environment variables.
- Not setting token expiry on JWTs, or accepting expired/invalid tokens silently instead of raising `401`.

## How to use

### App and route
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

### Pydantic schema with response model
```python
from pydantic import BaseModel, Field

class ItemIn(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class ItemOut(BaseModel):
    id: int
    name: str

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemIn):
    return {"id": 1, "name": item.name}
```

### Dependency example
```python
from fastapi import Depends

def get_token(token: str):
    return token

@app.get("/secure")
def secure(token: str = Depends(get_token)):
    return {"token": token}
```

### Background task
```python
from fastapi import BackgroundTasks

def save_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/submit")
def submit(background_tasks: BackgroundTasks):
    background_tasks.add_task(save_log, "submitted")
    return {"status": "queued"}
```

### JWT auth pattern (handler + bearer dependency)
```python
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET = "change-me"

def create_token(user_id: str) -> str:
    payload = {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(creds.credentials, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
```

### Middleware (request timing)
```python
import time
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.perf_counter() - start)
        return response

app.add_middleware(TimingMiddleware)
```

### CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myfrontend.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate limiting (slowapi)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/predict")
@limiter.limit("5/minute")
def predict(request: Request):
    return {"result": "..."}
```

### Testing with TestClient
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}
```
