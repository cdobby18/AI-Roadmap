"""Phase 6 - Basic RAG pipeline from scratch.

This example shows the full flow:
1. Chunk text
2. Create simple embeddings (TF-IDF)
3. Retrieve relevant chunks
4. Build a prompt with context
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def basic_rag(question: str, documents: list[str]):
    vectorizer = TfidfVectorizer()
    all_text = documents + [question]
    matrix = vectorizer.fit_transform(all_text)

    doc_vectors = matrix[:-1]
    query_vector = matrix[-1]

    scores = cosine_similarity(query_vector, doc_vectors).flatten()
    top_idx = scores.argsort()[-3:][::-1]

    context = "\n".join(documents[i] for i in top_idx)
    prompt = f"Answer the question using the context below.\n\nContext:\n{context}\n\nQuestion:\n{question}"

    return prompt


if __name__ == "__main__":
    docs = [
        "RAG stands for Retrieval-Augmented Generation.",
        "It improves answers by adding relevant retrieved context.",
        "Chunking and embeddings make retrieval more effective."
    ]

    print(basic_rag("What does RAG mean?", docs))
