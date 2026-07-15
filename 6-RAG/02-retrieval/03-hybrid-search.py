"""Phase 6 - Hybrid search.

Hybrid search combines keyword matching with semantic similarity.
This is useful because keyword search can find exact terms while semantic search
finds meaning-based matches.
"""

from typing import List, Tuple


def keyword_score(query: str, text: str) -> float:
    query_terms = set(query.lower().split())
    text_terms = set(text.lower().split())
    if not query_terms:
        return 0.0
    return len(query_terms & text_terms) / len(query_terms)


def hybrid_search(query: str, documents: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    scored = []
    for doc in documents:
        semantic = 0.7 if query.lower() in doc.lower() else 0.2
        keyword = keyword_score(query, doc)
        combined = semantic + keyword
        scored.append((doc, combined))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    docs = [
        "RAG improves answers with retrieved context.",
        "Keywords help exact match retrieval.",
        "Semantic search finds meaning beyond exact words."
    ]
    results = hybrid_search("semantic retrieval", docs)
    for doc, score in results:
        print(score, doc)
