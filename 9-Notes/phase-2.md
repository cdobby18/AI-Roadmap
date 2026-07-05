# Phase 2 — FastAPI

## Goal
Learn how to build an API backend that can serve AI or ML features.

## What I need to know
- FastAPI app structure
- GET/POST routes and path/query params
- Pydantic models for input validation
- Dependency injection with `Depends`
- Middleware and request lifecycle
- JWT and Basic Auth patterns
- Background tasks for non-blocking work

## Key terms
- `endpoint`: a route exposed by the API. Think of it as one URL that performs one job, like returning predictions or saving user input.
- `Pydantic`: the library that checks the shape of your incoming JSON. It prevents bad inputs from reaching your logic.
- `BaseModel`: the Pydantic class used to define input/output schemas. It is how you declare what data the API expects.
- `Depends`: FastAPI’s dependency injection helper. Use it to reuse logic like authentication, database connections, or configuration.
- `BackgroundTasks`: lets the server start a response immediately and run follow-up work later. It is useful for email sending, logging, or cache refresh.
- `JWT`: JSON Web Token. A compact, signed string that proves a user is authenticated without storing session state on the server.
- `HTTPException`: a way to stop the request and return an error code. Use it to handle invalid data, unauthorized access, or missing resources.
- `middleware`: code that runs before or after every request. Good middleware includes logging, timing, security headers, and CORS.

## When to use
- Use FastAPI when you need a web service for model inference.
- Use Pydantic whenever the API accepts JSON input.
- Use dependencies for shared logic like authentication.
- Use JWT for protected routes and user sessions.
- Use background tasks for logging, cache updates, or async side work.

## Interview review
- Explain that FastAPI is popular because it generates docs automatically and validates payloads before your endpoint code runs.
- If asked about `Depends`, say it is useful for injecting shared services without tight coupling.
- When talking about auth, describe the difference between cookie sessions and stateless JWT.
- Mention that background tasks are not for heavy CPU work; they are for I/O and deferred work.

## How to use

### App and route
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

### Pydantic schema
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

@app.post("/items")
def create_item(item: Item):
    return item
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

### Simple auth pattern
```python
from fastapi import HTTPException, status

if not valid:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
```
```
