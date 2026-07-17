"""Phase 6 — RAG Foundations: real semantic embeddings.

Uses sentence-transformers to create dense vector embeddings
and measures cosine similarity between queries and documents.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def basic_embedding_demo():
    documents = [
        "The cat sat on the mat.",
        "A dog slept beside the window.",
        "The cat is sleeping on the rug.",
        "Some dogs love to play fetch in the park.",
    ]

    doc_vectors = model.encode(documents)

    query = "cat sleeping"
    query_vec = model.encode([query])

    scores = cosine_similarity(query_vec, doc_vectors).flatten()

    print("Query:", query)
    print("Similarity scores:")
    for text, score in zip(documents, scores):
        print(f"  {score:.3f}  {text}")


if __name__ == "__main__":
    basic_embedding_demo()
