"""A simple retriever for RAG experiments."""

from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_chunks(query: str, chunks: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(chunks + [query])
    doc_vectors = matrix[:-1]
    query_vector = matrix[-1]

    scores = cosine_similarity(query_vector, doc_vectors).flatten()
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(chunks[i], score) for i, score in ranked[:top_k]]
