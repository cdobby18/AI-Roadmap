# 🚀 Phase 2: FastAPI + Web Development Fundamentals

This phase teaches you how to build **production-ready APIs** with FastAPI. You'll learn modern web development patterns, security best practices, and how to structure scalable applications.

> **Goal**: Master API development, authentication, and deployment-ready code patterns before moving to ML/AI systems.

---

## 📚 Learning Path Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  01-Basics                                                      │
│  Hello FastAPI: Routes, endpoints, and Swagger UI               │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  02-Routing-and-Validation                                      │
│  Pydantic models, request validation, proper HTTP semantics     │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  03-Advanced-Routing                                            │
│  APIRouter, middleware, persistent storage, CORS               │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  04-Authentication                                              │
│  ├─ 04a-Basic-Auth: HTTP Basic Authentication                 │
│  └─ 04b-JWT-Auth: Token-based stateless authentication        │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  05-Background-Tasks  ⭐ AI Engineering Core                   │
│  BackgroundTasks, lifespan model loading, async RAG, SSE       │
│  streaming — the patterns every LLM API is built on            │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Examples & Utils                                               │
│  Rate limiting, environment variables, logging, configurations │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 What You'll Learn

### Phase 2 Objectives

| Objective | Why It Matters | Examples |
|-----------|----------------|----------|
| **API Fundamentals** | APIs are how AI services communicate with clients | GET/POST endpoints, path & query parameters |
| **Data Validation** | Bad input breaks ML models - validate everything | Pydantic schemas, Field constraints |
| **Async/Await** | AI services need to handle many concurrent requests | `async def`, `await`, background tasks |
| **Authentication** | Secure your APIs - only authenticated users access data | Basic Auth, JWT tokens |
| **Project Structure** | Production-ready code organization | APIRouter, middleware, separation of concerns |
| **Middleware** | Add functionality across all requests (logging, timing, auth) | Custom middleware, CORS, rate limiting |
| **Error Handling** | Graceful error responses with proper HTTP status codes | HTTPException, validation errors |
| **Environment Config** | Never hardcode secrets - use environment variables | `.env` files, Pydantic Settings |

---

## 📂 Folder Structure

```
2-FastAPI/
├── 1-basics/                          # Start here: Hello FastAPI
│   └── main.py
│
├── 2-routing-and-validation/          # Pydantic & request bodies
│   └── main.py
│
├── 3-advanced-routing/                # Production patterns
│   ├── main.py
│   ├── storage.py
│   ├── schemas.py
│   ├── middleware/
│   │   └── timer.py
│   └── routes/
│       └── issues.py
│
├── 4-authentication/
│   ├── 4a-basic-auth/                # HTTP Basic Authentication
│   │   └── main.py
│   └── 4b-jwt-auth/                  # JWT Token Authentication
│       ├── main.py
│       ├── models.py
│       └── auth/
│           ├── jwt_handler.py
│           └── jwt_bearer.py
│
├── 5-background-tasks/               # ⭐ AI Engineering Core
│   └── main.py                       # BackgroundTasks, lifespan, async RAG, SSE streaming
│
├── examples/                          # Real-world patterns
│   ├── rate_limiting_example.py
│   └── env_variables_example.py
│
└── utils/                             # Helper functions
    ├── logger.py
    └── config.py
```

---

## 🚀 Quick Start

### Run Each Section

```bash
# 1. Basics
cd 1-basics
uvicorn main:app --reload
# Visit http://localhost:8000/docs

# 2. Routing & Validation
cd ../2-routing-and-validation
uvicorn main:app --reload

# 3. Advanced Routing
cd ../3-advanced-routing
uvicorn main:app --reload

# 4a. Basic Auth
cd ../4-authentication/4a-basic-auth
uvicorn main:app --reload

# 4b. JWT Auth
cd ../4-authentication/4b-jwt-auth
uvicorn main:app --reload

# 5. Background Tasks & Async Patterns
cd ../../5-background-tasks
uvicorn main:app --reload
```

---

## 📚 Key Concepts

### 1. **Routes & Parameters**

```python
# Path parameter
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# Query parameter
@app.get("/search")
def search(keyword: str, limit: int = 10):
    return {"keyword": keyword, "limit": limit}

# Request body
@app.post("/items")
def create_item(item: ItemSchema):
    return item
```

### 2. **Pydantic Validation**

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)  # Must be greater than 0
    stock: int = Field(default=0, ge=0)  # Greater than or equal to 0
```

### 3. **Dependency Injection**

```python
from fastapi import Depends

def get_current_user(token: str) -> str:
    # Validate token and return user
    return "user_id"

@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"user": user}
```

### 4. **Middleware**

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 5. **Async/Await**

```python
@app.get("/data")
async def get_data():
    # Can make concurrent requests
    result1 = await fetch_from_api_1()
    result2 = await fetch_from_api_2()
    return {"result1": result1, "result2": result2}
```

### 6. **Background Tasks (AI Core Pattern)**

```python
from fastapi import BackgroundTasks

def run_inference(job_id: str, text: str):
    result = model.predict(text)        # Runs after response is sent
    jobs[job_id] = {"status": "done", "result": result}

@app.post("/predict")
def predict(text: str, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_inference, job_id, text)
    return {"job_id": job_id, "status": "accepted"}  # Returns immediately
```

### 7. **Lifespan (Load Models Once)**

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    model["predict"] = load_heavy_model()  # Load at startup
    yield
    model.clear()                          # Cleanup at shutdown

app = FastAPI(lifespan=lifespan)
```

### 8. **SSE Streaming (LLM Token Streaming)**

```python
from fastapi.responses import StreamingResponse

async def token_generator(prompt: str):
    async for token in llm.stream(prompt):
        yield f"data: {token}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/chat")
async def chat(prompt: str):
    return StreamingResponse(token_generator(prompt), media_type="text/event-stream")
```

---

## 🔐 Authentication Patterns

### Basic Authentication
- Username + password in HTTP header
- Good for: Simple internal APIs
- Bad for: Public APIs (password exposed if HTTPS fails)

### JWT (JSON Web Token)
- Stateless token-based authentication
- Good for: Public APIs, mobile apps, microservices
- Token format: `Header.Payload.Signature`

```python
# Login: get token
POST /auth/login
{"email": "user@example.com", "password": "pass123"}
→ {"access_token": "eyJ0eX..."}

# Use token: send in Authorization header
GET /protected
Headers: {"Authorization": "Bearer eyJ0eX..."}
```

---

## 📦 Dependencies

```bash
# Core
pip install fastapi uvicorn pydantic

# Authentication
pip install python-jose passlib bcrypt PyJWT

# Database (later phases)
pip install sqlalchemy

# Rate limiting
pip install slowapi

# Environment variables
pip install python-dotenv

# Development
pip install pytest pytest-asyncio httpx
```

---

## 🧪 Testing Your APIs

### Using Swagger UI
- **Automatic**: FastAPI generates interactive docs at `/docs`
- **Manual testing**: Click "Try it out" button
- **Authorization**: Click "Authorize" button to use credentials

### Using curl

```bash
# GET request
curl http://localhost:8000/items

# POST with JSON
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "item", "price": 9.99}'

# With Authorization header (JWT)
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/protected
```

### Using Python httpx

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/items")
    print(response.json())
```

---

## 🔗 Recommended Resources

| Resource | What You Get | Format | Cost |
|----------|-------------|--------|------|
| [FastAPI Official Docs](https://fastapi.tiangolo.com/) | Complete reference, tutorials, examples | Docs | Free |
| [ArjanCodes - FastAPI Tutorial](https://www.youtube.com/watch?v=7t2alWjYm6I) | Senior-level FastAPI patterns | Video | Free |
| [Real Python - FastAPI intro](https://realpython.com/fastapi-python-web-apis/) | Beginner-friendly introduction | Article | Free |
| [Pydantic Official Docs](https://docs.pydantic.dev/) | Data validation reference | Docs | Free |
| [JWT.io Introduction](https://jwt.io/introduction) | Understand JWT tokens | Article | Free |
| [OAuth 2.0 for Beginners](https://www.oauth.com/oauth2-servers/) | Modern authentication patterns | Article | Free |

---

## 🎓 Learning Progression

### Week 1: Foundations
- [ ] Understand HTTP methods (GET, POST, PUT, DELETE)
- [ ] Create basic routes in FastAPI
- [ ] Learn path vs query vs body parameters
- [ ] Test APIs using Swagger UI

### Week 2: Validation & Structure
- [ ] Use Pydantic for request validation
- [ ] Create response models
- [ ] Organize routes with APIRouter
- [ ] Implement proper error handling

### Week 3: Advanced Patterns
- [ ] Add middleware (CORS, logging, timing)
- [ ] Implement persistent storage
- [ ] Use async/await effectively
- [ ] Create modular, production-ready structure

### Week 4: Security
- [ ] Implement HTTP Basic Authentication
- [ ] Generate and validate JWT tokens
- [ ] Create protected endpoints
- [ ] Use environment variables for secrets

### Week 5: Async & AI Patterns
- [ ] Understand sync vs async inference trade-offs
- [ ] Use `BackgroundTasks` for fire-and-forget jobs
- [ ] Load ML models with lifespan events
- [ ] Implement async RAG (concurrent retrieval + LLM call)
- [ ] Stream LLM responses with Server-Sent Events

### Week 6+: Real-World Projects
- [ ] Build a complete API with database
- [ ] Integrate with ML models
- [ ] Deploy to production
- [ ] Monitor and log requests

---

## ✅ Checklist: By End of Phase 2

- [ ] Can create GET/POST/PUT/DELETE endpoints
- [ ] Understand Pydantic validation
- [ ] Know difference between path/query/body parameters
- [ ] Can structure large FastAPI projects
- [ ] Understand async/await and why it matters
- [ ] Can implement HTTP Basic Auth
- [ ] Can implement JWT authentication
- [ ] Know how to use middleware
- [ ] Can handle errors gracefully
- [ ] Can manage configuration with environment variables
- [ ] Can offload slow work with BackgroundTasks
- [ ] Can load ML models once with lifespan events
- [ ] Can stream LLM responses with Server-Sent Events

---

## 🚨 Common Mistakes

| Mistake | Why It's Bad | Solution |
|---------|------------|----------|
| Hardcoding secrets | Exposed in version control | Use environment variables |
| Not validating input | Bad data breaks ML models | Use Pydantic schemas |
| Ignoring async/await | Slow, can't handle concurrent requests | Always use async for I/O |
| Missing error handling | Users get confusing 500 errors | Use HTTPException with proper status codes |
| No logging | Can't debug production issues | Add logging at key points |
| Mixing business logic with routes | Hard to test and maintain | Keep routes thin, move logic to functions |

---

## 🎯 Phase 2 Success Criteria

✅ You're ready for Phase 3 when you can:
1. Build a complete CRUD API with proper structure
2. Validate all inputs with Pydantic
3. Implement authentication (choose Basic or JWT)
4. Handle errors gracefully
5. Write async endpoints
6. Organize code with routers and middleware
7. Use environment variables for configuration
8. Test your API thoroughly

---

## 🔥 Challenge Projects

### Project 1: Todo API
- Create CRUD endpoints for todos
- Add priority and status fields
- Implement filtering by status
- Validate all inputs
- Store in JSON file

### Project 2: User Registration API
- Signup endpoint with email validation
- Login endpoint with JWT token
- Protected endpoint that returns user profile
- Password hashing with bcrypt
- Token expiration

### Project 3: Simple Blog API
- Post CRUD endpoints
- User authentication
- Posts can only be edited by author
- Comments on posts (nested resources)
- Rate limiting on post creation

---
