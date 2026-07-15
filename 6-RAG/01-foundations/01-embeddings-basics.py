"""Phase 6 - RAG Foundations: embeddings and similarity.

This file introduces the core idea behind RAG: turning text into vectors
and measuring how close different pieces of text are.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def basic_embedding_demo():
    documents = [
        "The cat sat on the mat.",
        "A dog slept beside the window.",
        "The cat is sleeping on the rug."
    ]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    query = "cat sleeping"
    query_vec = vectorizer.transform([query])

    scores = cosine_similarity(query_vec, vectors).flatten()

    print("Query:", query)
    print("Similarity scores:")
    for text, score in zip(documents, scores):
        print(f"- {text} -> {score:.3f}")


if __name__ == "__main__":
    basic_embedding_demo()
