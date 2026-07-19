"""FastAPI app for Phase 6 RAG with real LLM integration."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.rag_config import (
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    REWRITER_STRATEGY,
    DEFAULT_TOP_K,
)
from app.retriever import retrieve_relevant_chunks
from app.ollama_client import generate_with_ollama
from app.query_rewriter import QueryRewriter

app = FastAPI(title="Phase 6 RAG Demo", version="0.3.0")
_rewriter = QueryRewriter(strategy=REWRITER_STRATEGY)


class QuestionRequest(BaseModel):
    question: str
    top_k: int = DEFAULT_TOP_K
    model: str = "llama2"
    rewrite_strategy: str | None = None
    history: list[str] | None = None
    metadata_filter: dict | None = None


class AnswerResponse(BaseModel):
    question: str
    rewritten_query: str | None = None
    context_chunks: list[str]
    sources: list[str]
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG demo is running"}


@app.get("/embedding-profile")
def get_embedding_profile():
    from app.rag_config import EMBEDDING_MODEL_PROFILE, EMBEDDING_MODEL_OPTIONS
    return {
        "active_profile": EMBEDDING_MODEL_PROFILE,
        "model": EMBEDDING_MODEL_OPTIONS.get(EMBEDDING_MODEL_PROFILE, "unknown"),
        "available_profiles": list(EMBEDDING_MODEL_OPTIONS.keys()),
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    rewriter = _rewriter
    if request.rewrite_strategy is not None:
        rewriter.strategy = request.rewrite_strategy

    rewritten = rewriter.rewrite(request.question, history=request.history)

    chunks = []
    for source, content in load_text_files(DATA_DIR):
        chunks.extend(chunk_text(content, source=source, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP))

    retrieved = retrieve_relevant_chunks(
        rewritten, chunks, top_k=request.top_k, metadata_filter=request.metadata_filter,
    )
    context_chunks = [c.text for c, _ in retrieved]
    sources = list({c.source for c, _ in retrieved})

    context = "\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{request.question}
"""

    answer = generate_with_ollama(prompt, model=request.model)
    return AnswerResponse(
        question=request.question,
        rewritten_query=rewritten,
        context_chunks=context_chunks,
        sources=sources,
        answer=answer,
    )