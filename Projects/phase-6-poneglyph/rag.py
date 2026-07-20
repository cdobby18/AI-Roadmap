"""RAG pipeline — retrieval, reranking, and answer generation.

This is the core of the Poneglyph Reader. The pipeline:

1. Query rewriting — If there's chat history, rewrite the question to be
   self-contained (e.g., "Who is he?" -> "Who is Gol D. Roger?")

2. Vector search — Embed the query, find the top-K most similar chunks
   in ChromaDB using cosine similarity

3. Reranking — Re-rank the retrieved chunks with a cross-encoder for
   better precision (the bi-encoder is fast but approximate; the
   cross-encoder is slower but more accurate)

4. Answer generation — Pack the top chunks as context into a prompt,
   send to the LLM, return the answer with source citations

This pattern — retrieve → rerank → generate — is the standard production
RAG architecture used by companies like Glean, Notion AI, and Perplexity.
"""

import json
import re
from typing import List, Optional, Tuple

import requests
from sentence_transformers import CrossEncoder

from config import (
    CHROMA_DIR,
    EMBEDDING_MODEL,
    HF_MODEL,
    HF_TOKEN,
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_TEMPERATURE,
    OLLAMA_BASE_URL,
    RERANKER_MODEL,
    TOP_K_RERANK,
    TOP_K_RETRIEVAL,
)
from ingestion import embed, get_collection

try:
    from huggingface_hub import InferenceClient
    HF_CLIENT = InferenceClient(token=HF_TOKEN) if HF_TOKEN else InferenceClient()
except ImportError:
    HF_CLIENT = None


# -------------------------------------------------------------------
# 1. Query rewriting
# -------------------------------------------------------------------

def rewrite_query(question: str, history: Optional[List[str]] = None) -> str:
    """Rewrite a question to be self-contained using conversation history.

    Why rewrite?
    - Users ask follow-ups like "What about his crew?" without context
    - The vector search needs a standalone query to find relevant chunks
    - Rewriting resolves pronouns and implicit references into explicit terms
    """
    if not history:
        return question

    history_text = "\n".join(history[-6:])
    prompt = f"""Rewrite this question as a standalone search query.
If it's already standalone, return it unchanged.

Chat history:
{history_text}

Question: {question}

Standalone query:"""

    answer = _call_llm(prompt)
    return answer.strip() or question


# -------------------------------------------------------------------
# 2. Vector search
# -------------------------------------------------------------------

def search(
    query: str,
    top_k: int = TOP_K_RETRIEVAL,
    category_filter: Optional[str] = None,
) -> List[Tuple[str, str, float]]:
    """Search ChromaDB for chunks similar to the query.

    Returns list of (text, source, score) tuples, sorted by relevance.

    How vector search works:
    1. Encode the query into an embedding vector (same model as ingestion)
    2. ChromaDB finds the top-K nearest neighbors using cosine similarity
    3. Each result has a distance score (lower = more similar)

    Metadata filtering:
    - We can filter by category (e.g., only "character" pages)
    - ChromaDB applies the filter before or during the search
    """
    collection = get_collection()
    query_vec = embed([query])

    where = None
    if category_filter:
        where = {"categories": {"$contains": category_filter}}

    results = collection.query(
        query_embeddings=query_vec,
        n_results=top_k,
        where=where,
    )

    if not results or not results.get("documents"):
        return []

    chunks = []
    for i in range(len(results["documents"][0])):
        text = results["documents"][0][i]
        source = ""
        metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
        if metadata:
            source = metadata.get("source", "")
        distance = results["distances"][0][i] if results.get("distances") else 0.0
        # Convert distance to similarity score (cosine distance → similarity)
        score = 1.0 - distance
        chunks.append((text, source, score))

    return chunks


# -------------------------------------------------------------------
# 3. Reranking with cross-encoder
# -------------------------------------------------------------------

_reranker = None


def get_reranker() -> CrossEncoder:
    """Lazy-load the cross-encoder reranker."""
    global _reranker
    if _reranker is None:
        print(f"Loading reranker: {RERANKER_MODEL}")
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def rerank(
    query: str,
    candidates: List[Tuple[str, str, float]],
    top_k: int = TOP_K_RERANK,
) -> List[Tuple[str, str, float]]:
    """Re-rank candidates using a cross-encoder for better precision.

    Why rerank?
    - Bi-encoder (used in vector search) embeds query and doc separately
      → fast but loses cross-attention between query and doc
    - Cross-encoder processes (query, doc) pairs together → slower but
      much more accurate at judging relevance
    - Typical setup: bi-encoder retrieves top-50, cross-encoder re-ranks
      top-10 for the final answer
    """
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, text) for text, _, _ in candidates]
    scores = model.predict(pairs)

    ranked = sorted(
        zip([text for text, _, _ in candidates],
            [src for _, src, _ in candidates],
            scores),
        key=lambda x: x[2],
        reverse=True,
    )
    return [(text, src, float(score)) for text, src, score in ranked[:top_k]]


# -------------------------------------------------------------------
# 4. LLM call
# -------------------------------------------------------------------

def _call_llm_ollama(prompt: str) -> str:
    """Call Ollama's generate endpoint."""
    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": LLM_TEMPERATURE},
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    except requests.RequestException as e:
        return f"[Ollama unavailable: {e}]"


def _call_llm_hf(prompt: str) -> str:
    """Call HuggingFace Inference API."""
    if HF_CLIENT is None:
        return "[HF Inference API unavailable: install huggingface_hub]"
    try:
        result = HF_CLIENT.text_generation(
            prompt,
            model=HF_MODEL,
            max_new_tokens=512,
            temperature=LLM_TEMPERATURE,
        )
        return result
    except Exception as e:
        return f"[HF Inference API error: {e}]"


def _call_llm(prompt: str) -> str:
    """Route to the configured LLM backend."""
    if LLM_PROVIDER == "hf_inference":
        return _call_llm_hf(prompt)
    return _call_llm_ollama(prompt)


# -------------------------------------------------------------------
# 5. Full RAG pipeline
# -------------------------------------------------------------------

def ask(
    question: str,
    history: Optional[List[str]] = None,
    category_filter: Optional[str] = None,
    use_reranker: bool = True,
) -> dict:
    """Full RAG pipeline: rewrite → search → rerank → generate.

    Returns a dict with:
        question         — original question
        rewritten_query  — query after rewriting (if history existed)
        chunks           — list of (text, source, score) used as context
        answer           — LLM-generated answer
        sources          — unique source URLs for citations
    """
    # Step 1: Rewrite query if there's history
    rewritten = rewrite_query(question, history) if history else question

    # Step 2: Vector search
    candidates = search(rewritten, category_filter=category_filter)

    # Step 3: Rerank for precision
    if use_reranker and candidates:
        chunks = rerank(rewritten, candidates)
    else:
        chunks = candidates

    if not chunks:
        return {
            "question": question,
            "rewritten_query": rewritten if history else None,
            "chunks": [],
            "answer": "I couldn't find any relevant information to answer that.",
            "sources": [],
        }

    # Step 4: Build context and generate answer
    context = "\n\n".join(
        f"[Source {i+1}] {text}"
        for i, (text, src, score) in enumerate(chunks)
    )

    prompt = f"""You are a knowledgeable One Piece scholar. Answer the question using ONLY the context provided.
If the context doesn't contain enough information, say so.
When you use information from a source, cite it as [Source 1], [Source 2], etc.

Context:
{context}

Question: {question}

Answer:"""

    answer = _call_llm(prompt)

    # Extract unique sources for citations
    sources = list(dict.fromkeys([src for _, src, _ in chunks]))

    return {
        "question": question,
        "rewritten_query": rewritten if history else None,
        "chunks": [(text, src, round(score, 3)) for text, src, score in chunks],
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    result = ask("Who is Monkey D. Luffy?")
    print(f"Q: {result['question']}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
