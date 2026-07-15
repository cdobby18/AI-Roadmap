"""Phase 6 - Reranking.

Reranking is used after initial retrieval to improve the final ranking.
This example demonstrates a simple reranking step based on a bonus for exact phrase matches.
"""

from typing import List, Tuple


def rerank_results(query: str, results: List[Tuple[str, float]], top_k: int = 3) -> List[Tuple[str, float]]:
    reranked = []
    for text, score in results:
        phrase_bonus = 0.2 if query.lower() in text.lower() else 0.0
        reranked.append((text, score + phrase_bonus))
    reranked.sort(key=lambda item: item[1], reverse=True)
    return reranked[:top_k]


if __name__ == "__main__":
    initial = [
        ("RAG uses retrieval to improve answers", 0.7),
        ("A summary of retrieval systems", 0.6),
        ("This text mentions RAG explicitly", 0.5),
    ]
    print(rerank_results("RAG", initial))
