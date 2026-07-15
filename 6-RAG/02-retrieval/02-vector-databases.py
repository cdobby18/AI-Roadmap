"""Phase 6 - Vector DB introduction.

This file explains the role of vector databases in RAG systems.
It uses a simple in-memory example instead of a real database.
"""

from typing import List, Tuple


class SimpleVectorStore:
    def __init__(self):
        self.docs: List[str] = []
        self.vectors: List[List[float]] = []

    def add(self, text: str, vector: List[float]):
        self.docs.append(text)
        self.vectors.append(vector)

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        scores = []
        for stored_vector in self.vectors:
            dot = sum(a * b for a, b in zip(stored_vector, query_vector))
            scores.append(dot)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return [(self.docs[i], scores[i]) for i, _ in ranked[:top_k]]


if __name__ == "__main__":
    store = SimpleVectorStore()
    store.add("RAG uses external context", [0.9, 0.1])
    store.add("FastAPI builds APIs", [0.2, 0.8])
    store.add("Embeddings convert text to vectors", [0.7, 0.3])

    results = store.search([0.8, 0.2], top_k=2)
    for text, score in results:
        print(text, score)
