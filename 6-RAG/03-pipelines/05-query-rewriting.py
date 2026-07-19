"""Phase 6 - Query rewriting for RAG.

Raw user queries are often ambiguous, conversational, or poorly aligned with
the embedding space. Query rewriting transforms them before retrieval to get
better results.

Two strategies covered here:
1. Standalone rewriting — converts context-dependent queries into self-contained ones
2. HyDE (Hypothetical Document Embeddings) — generates a hypothetical answer chunk
   and uses ITS embedding for retrieval, bridging the query-document gap
"""

from sentence_transformers import SentenceTransformer, util
import numpy as np


# ---------------------------------------------------------------------------
# Standalone rewriting
# ---------------------------------------------------------------------------

def rewrite_standalone(question: str, history: list[str] | None = None) -> str:
    """Rewrite a conversational query into a standalone search query.

    In production this would call an LLM. Here we simulate with a simple
    rule-based approach for illustration.
    """
    if not history:
        return question

    pronouns = {"it", "this", "that", "they", "them", "those", "these"}
    first_word = question.strip().lower().split()[0] if question.strip() else ""

    if first_word in pronouns or question.strip().startswith(("what about", "tell me more", "how about")):
        last_topic = _extract_last_topic(history)
        return f"{question} — specifically regarding {last_topic}"

    followup_starters = {"and", "but", "or", "so", "also", "then", "why", "how"}
    is_followup = any(question.strip().lower().startswith(w) for w in followup_starters)
    if is_followup:
        last_topic = _extract_last_topic(history)
        return f"{question} [{last_topic}]"

    return question


def _extract_last_topic(history: list[str]) -> str:
    for turn in reversed(history):
        if turn.startswith("User:"):
            return turn.replace("User:", "").strip()
    return "the previous topic"


# ---------------------------------------------------------------------------
# HyDE — Hypothetical Document Embeddings
# ---------------------------------------------------------------------------

def generate_hypothetical_document(question: str) -> str:
    """Generate a hypothetical document that would answer the question.

    In production this calls an LLM. Here we return a template to show
    the concept.
    """
    return (
        f"This document contains information about: {question}. "
        f"It explains the key concepts, provides examples, and discusses "
        f"important details related to this topic. The answer covers "
        f"definitions, use cases, and practical implications."
    )


def retrieve_with_hyde(
    question: str,
    chunks: list[str],
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[str, float]]:
    """HyDE retrieval: embed a hypothetical document instead of the query."""
    hypo_doc = generate_hypothetical_document(question)
    hypo_emb = model.encode(hypo_doc, convert_to_numpy=True)
    chunk_embs = model.encode(chunks, convert_to_numpy=True)

    scores = util.cos_sim(hypo_emb, chunk_embs).numpy().flatten()
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [(chunks[i], float(scores[i])) for i in top_indices]


# ---------------------------------------------------------------------------
# Comparison demo
# ---------------------------------------------------------------------------

def compare_strategies(question: str, history: list[str], chunks: list[str]):
    print("=" * 60)
    print(f"Original question: {question!r}")
    print(f"History: {history[-2:]}")
    print("=" * 60)

    standalone = rewrite_standalone(question, history)
    print(f"\n1. Standalone rewrite: {standalone!r}")

    hypo = generate_hypothetical_document(question)
    print(f"\n2. HyDE hypothetical doc (first 120 chars):")
    print(f"   {hypo[:120]}...")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    q_emb = model.encode(question, convert_to_numpy=True)
    s_emb = model.encode(standalone, convert_to_numpy=True)
    h_emb = model.encode(hypo, convert_to_numpy=True)

    print(f"\n3. Retrieval similarity (top-3 chunks):")
    chunk_embs = model.encode(chunks, convert_to_numpy=True)

    for label, emb in [("Original query", q_emb), ("Standalone", s_emb), ("HyDE doc", h_emb)]:
        scores = util.cos_sim(emb, chunk_embs).numpy().flatten()
        top_idx = np.argsort(scores)[-3:][::-1]
        print(f"\n   {label}:")
        for i in top_idx:
            print(f"      {scores[i]:.3f}  {chunks[i][:60]}...")


if __name__ == "__main__":
    sample_chunks = [
        "Sentence-transformers produce dense vector embeddings for semantic similarity.",
        "FAISS is a library for efficient similarity search and clustering of dense vectors.",
        "Cross-encoder rerankers jointly encode query and document for precise relevance scoring.",
        "Query rewriting transforms user questions to improve retrieval quality.",
        "HyDE generates a hypothetical document to bridge the query-document gap.",
        "Chunking strategy is the most important factor in RAG pipeline performance.",
        "Metadata filtering tags chunks with source, date, and section for targeted retrieval.",
        "Cosine similarity measures the angle between two embedding vectors.",
    ]

    history = [
        "User: What is a cross-encoder?",
        "Assistant: A cross-encoder jointly processes query and document through attention layers.",
    ]

    compare_strategies("How does it compare to a bi-encoder?", history, sample_chunks)
