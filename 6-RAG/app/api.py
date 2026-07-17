"""FastAPI app for Phase 6 RAG with real LLM integration."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.rag_config import DATA_DIR
from app.retriever import retrieve_relevant_chunks
from app.ollama_client import generate_with_ollama

app = FastAPI(title="Phase 6 RAG Demo", version="0.2.0")


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3
    model: str = "llama2"


class AnswerResponse(BaseModel):
    question: str
    context_chunks: list[str]
    answer: str


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
        context_chunks=context_chunks,
        answer=answer,
    )
