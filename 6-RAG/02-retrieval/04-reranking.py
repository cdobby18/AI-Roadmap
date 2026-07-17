"""Phase 6 — Cross-encoder reranking for RAG.

A cross-encoder scores query-document pairs jointly, giving
more accurate relevance judgments than cosine similarity alone.
"""

from sentence_transformers import CrossEncoder


def rerank_documents(query: str, documents: list[str], top_k: int = 3):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    pairs = [(query, doc) for doc in documents]
    scores = model.predict(pairs)
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


if __name__ == "__main__":
    docs = [
        "RAG uses retrieval to provide context before generation.",
        "Python is a general-purpose programming language.",
        "Cross-encoders score query-document pairs more accurately.",
        "FastAPI is a modern web framework for building APIs.",
    ]
    results = rerank_documents("How does RAG work?", docs)
    for doc, score in results:
        print(f"{score:.3f}  {doc}")
