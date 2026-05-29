"""
05 - BACKGROUND TASKS & ASYNC PATTERNS

Learn:
- FastAPI BackgroundTasks for fire-and-forget work
- Lifespan events (startup/shutdown) for model loading
- Async endpoints for concurrent I/O
- Server-Sent Events (SSE) for streaming AI responses
- Job queue pattern for long-running AI inference

Why this matters for AI Engineering:
- ML model inference is slow — never block the HTTP response
- LLM token streaming improves perceived latency
- Models should be loaded once at startup, not per request
- Multiple users hitting inference simultaneously needs async handling

Run: uvicorn main:app --reload
Visit: http://localhost:8000/docs
"""

import asyncio
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


# ================================
# LIFESPAN: Load model at startup
# ================================
# In real AI apps, load your model ONCE here — not inside each request handler.
# This saves seconds per request and avoids memory spikes.

ml_model = {}  # Simulates a loaded model (e.g., transformers pipeline)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: load the ML model into memory.
    Shutdown: clean up resources.

    Real usage:
        from transformers import pipeline
        ml_model["classifier"] = pipeline("sentiment-analysis")
    """
    print("Loading ML model into memory...")
    ml_model["predict"] = lambda text: {
        "label": "POSITIVE" if len(text) % 2 == 0 else "NEGATIVE",
        "score": 0.97
    }
    print("Model loaded. API ready.")
    yield
    # Cleanup on shutdown
    ml_model.clear()
    print("Model unloaded. Shutdown complete.")


app = FastAPI(
    title="05 - Background Tasks & Async Patterns",
    description="AI-relevant async patterns: background jobs, streaming, model inference",
    version="5.0.0",
    lifespan=lifespan
)


# ================================
# SCHEMAS
# ================================

class InferenceRequest(BaseModel):
    text: str
    job_id: str | None = None

    class Config:
        schema_extra = {"example": {"text": "FastAPI makes building AI APIs easy!"}}


class JobStatus(BaseModel):
    job_id: str
    status: str      # "pending" | "running" | "done" | "failed"
    result: dict | None = None


# In-memory job store (use Redis in production)
jobs: dict[str, JobStatus] = {}


# ================================
# PATTERN 1: Synchronous (bad for AI)
# ================================

@app.post("/predict/sync")
def predict_sync(request: InferenceRequest):
    """
    BLOCKING prediction — the HTTP connection stays open during inference.
    Bad for: slow models (GPT-4, image generation, embeddings).
    Fine for: fast models (<100ms) or development.
    """
    if "predict" not in ml_model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    time.sleep(0.1)  # Simulate model inference latency
    result = ml_model["predict"](request.text)
    return {"result": result, "pattern": "sync — blocks until done"}


# ================================
# PATTERN 2: BackgroundTasks (fire and forget)
# ================================

def run_inference_job(job_id: str, text: str):
    """
    Runs in the background after the HTTP response is already sent.
    Use for: sending emails, logging, triggering pipelines, slow inference.
    """
    jobs[job_id].status = "running"
    time.sleep(2)  # Simulate slow inference (e.g., LLM call)

    result = ml_model["predict"](text)
    jobs[job_id].status = "done"
    jobs[job_id].result = result


@app.post("/predict/async", status_code=status.HTTP_202_ACCEPTED)
def predict_async(request: InferenceRequest, background_tasks: BackgroundTasks):
    """
    Returns immediately with a job ID. Inference runs in the background.
    Client polls GET /jobs/{job_id} to check status.

    This is the standard pattern for:
    - LLM completions
    - Image generation
    - Document processing
    - Embedding generation for large batches
    """
    job_id = str(uuid.uuid4())
    jobs[job_id] = JobStatus(job_id=job_id, status="pending")

    background_tasks.add_task(run_inference_job, job_id, request.text)

    return {
        "job_id": job_id,
        "status": "accepted",
        "poll_url": f"/jobs/{job_id}",
        "message": "Inference started. Poll the job URL for results."
    }


@app.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str):
    """Poll this endpoint to check inference job status."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]


# ================================
# PATTERN 3: Async endpoint (concurrent I/O)
# ================================

async def fetch_external_context(query: str) -> dict:
    """Simulate an async call to a vector DB or external API."""
    await asyncio.sleep(0.05)  # Non-blocking I/O wait
    return {"context": f"Relevant docs for: {query}", "source": "vector_db"}


async def call_llm_api(prompt: str) -> dict:
    """Simulate an async LLM API call (e.g., OpenAI, Anthropic)."""
    await asyncio.sleep(0.2)  # Non-blocking wait for API response
    return {"completion": f"AI response to: {prompt[:50]}..."}


@app.post("/predict/rag")
async def predict_with_rag(request: InferenceRequest):
    """
    Async RAG (Retrieval-Augmented Generation) pattern.

    Fetches context from vector DB and calls LLM concurrently using asyncio.gather.
    Without async: 250ms sequential. With async: ~200ms concurrent.

    This is the foundation of every AI chatbot backend.
    """
    # Run both I/O calls concurrently (not sequentially)
    context, _ = await asyncio.gather(
        fetch_external_context(request.text),
        asyncio.sleep(0)  # Placeholder for auth/logging
    )

    # Call LLM with retrieved context
    augmented_prompt = f"Context: {context['context']}\n\nQuestion: {request.text}"
    response = await call_llm_api(augmented_prompt)

    return {
        "answer": response["completion"],
        "context_used": context["context"],
        "pattern": "async RAG — concurrent context retrieval + LLM call"
    }


# ================================
# PATTERN 4: Streaming response (SSE)
# ================================

async def token_stream_generator(prompt: str) -> AsyncGenerator[str, None]:
    """
    Simulates token-by-token streaming from an LLM.

    Real usage with Anthropic SDK:
        async with client.messages.stream(...) as stream:
            async for text in stream.text_stream:
                yield f"data: {text}\n\n"
    """
    fake_tokens = f"Response to [{prompt[:30]}]: The answer is ".split() + [
        "generated", "token", "by", "token", "for", "better", "UX", "."
    ]

    for token in fake_tokens:
        yield f"data: {token}\n\n"
        await asyncio.sleep(0.1)  # Simulate per-token generation delay

    yield "data: [DONE]\n\n"


@app.post("/predict/stream")
async def predict_stream(request: InferenceRequest):
    """
    Streams the response token-by-token using Server-Sent Events (SSE).

    Why: Users see output immediately instead of waiting for the full response.
    This is how ChatGPT, Claude.ai, and every modern LLM UI works.

    Client reads: EventSource or fetch with ReadableStream.
    Each event: "data: <token>\\n\\n"
    End signal: "data: [DONE]\\n\\n"
    """
    return StreamingResponse(
        token_stream_generator(request.text),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


# ================================
# HEALTH & READINESS
# ================================

@app.get("/")
def root():
    return {
        "message": "Background Tasks & Async Patterns Demo",
        "model_loaded": "predict" in ml_model,
        "patterns": {
            "sync": "POST /predict/sync",
            "async_job": "POST /predict/async → GET /jobs/{id}",
            "rag": "POST /predict/rag",
            "streaming": "POST /predict/stream"
        }
    }


@app.get("/health")
def health():
    """Readiness check — used by Kubernetes/load balancers."""
    if "predict" not in ml_model:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"status": "ready", "model": "loaded"}


# ================================
# HOW TO TEST
# ================================
# 1. Sync (blocks):
#    curl -X POST /predict/sync -d '{"text": "hello world"}'
#
# 2. Async job:
#    curl -X POST /predict/async -d '{"text": "hello world"}'
#    → {"job_id": "abc123", "poll_url": "/jobs/abc123"}
#    curl /jobs/abc123   # poll until status == "done"
#
# 3. RAG pattern:
#    curl -X POST /predict/rag -d '{"text": "What is RAG?"}'
#
# 4. Streaming (in terminal):
#    curl -N -X POST /predict/stream -H "Content-Type: application/json" \
#         -d '{"text": "Tell me about FastAPI"}'
