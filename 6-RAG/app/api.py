"""A simple FastAPI app for the Phase 6 RAG example.

This exposes the retrieval + prompt-building flow over HTTP so you can
see how a RAG pipeline can be wrapped in a small backend service.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.rag_config import DATA_DIR
from app.retriever import retrieve_relevant_chunks

app = FastAPI(title="Phase 6 RAG Demo", version="0.1.0")


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


class AnswerResponse(BaseModel):
    question: str
    context_chunks: list[str]
    prompt: str


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG demo is running"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    documents = load_text_files(DATA_DIR)
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc))

    retrieved = retrieve_relevant_chunks(request.question, chunks, top_k=request.top_k)
    context_chunks = [chunk for chunk, _ in retrieved]

    prompt = "\n\n".join(context_chunks)
    return AnswerResponse(
        question=request.question,
        context_chunks=context_chunks,
        prompt=prompt,
    )
