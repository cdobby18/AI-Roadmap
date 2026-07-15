"""Phase 6 - Retrieval: semantic search basics.

This example demonstrates a simple retrieval flow using TF-IDF vectors.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_docs(query: str, documents: list[str], top_k: int = 3):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(documents + [query])

    doc_vectors = matrix[:-1]
    query_vector = matrix[-1]

    scores = cosine_similarity(query_vector, doc_vectors).flatten()
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    return [(documents[i], score) for i, score in ranked[:top_k]]


if __name__ == "__main__":
    docs = [
        "Python is a popular programming language.",
        "RAG uses retrieval to improve language model answers.",
        "FastAPI helps build APIs quickly.",
        "Embeddings represent text as vectors."
    ]

    results = retrieve_relevant_docs("How does retrieval improve answers?", docs)
    for doc, score in results:
        print(f"{doc} -> {score:.3f}")
