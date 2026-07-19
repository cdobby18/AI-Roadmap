"""End-to-end RAG pipeline with real embeddings and LLM call."""

from __future__ import annotations

from typing import List

from app.chunker import chunk_text, Chunk
from app.document_loader import load_text_files
from app.retriever import retrieve_relevant_chunks
from app.rag_config import (
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    REWRITER_STRATEGY,
    DEFAULT_TOP_K,
)
from app.ollama_client import generate_with_ollama
from app.query_rewriter import QueryRewriter


_rewriter: QueryRewriter | None = None


def _get_rewriter() -> QueryRewriter:
    global _rewriter
    if _rewriter is None:
        _rewriter = QueryRewriter(strategy=REWRITER_STRATEGY)
    return _rewriter


def _load_and_chunk(data_dir: str = DATA_DIR) -> List[Chunk]:
    chunks: List[Chunk] = []
    for source, content in load_text_files(data_dir):
        chunks.extend(chunk_text(content, source=source, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP))
    return chunks


def ask(
    question: str,
    top_k: int = DEFAULT_TOP_K,
    model: str = "llama2",
    history: list[str] | None = None,
    rewrite_strategy: str | None = None,
    metadata_filter: dict | None = None,
) -> dict:
    rewriter = _get_rewriter()
    if rewrite_strategy is not None:
        rewriter.strategy = rewrite_strategy

    rewritten = rewriter.rewrite(question, history=history)
    chunks = _load_and_chunk()

    retrieved = retrieve_relevant_chunks(
        rewritten, chunks, top_k=top_k, metadata_filter=metadata_filter,
    )
    context_chunks = [chunk for chunk, _ in retrieved]
    scores = [score for _, score in retrieved]
    context = "\n\n".join(c.text for c in context_chunks)
    sources = list({c.source for c in context_chunks})

    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}
"""
    answer = generate_with_ollama(prompt, model=model)
    return {
        "question": question,
        "rewritten_query": rewritten,
        "context": context_chunks,
        "scores": scores,
        "sources": sources,
        "answer": answer,
    }


if __name__ == "__main__":
    result = ask("What is chunking and why does it matter?")
    print(f"Q: {result['question']}")
    print(f"  (rewritten: {result['rewritten_query']})")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")