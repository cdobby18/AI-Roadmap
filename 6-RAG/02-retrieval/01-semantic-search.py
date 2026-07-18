"""Phase 6 - Semantic search with sentence embeddings + FAISS.

Semantic search means finding documents by meaning, not keywords.
This uses sentence-transformers (dense embeddings) + FAISS (fast search).
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

DOCUMENTS = [
    "Python is a popular programming language used for data science and web development.",
    "RAG uses retrieval to give LLMs relevant context before generating an answer.",
    "FastAPI is a modern Python web framework with automatic OpenAPI documentation.",
    "Embeddings represent text as dense vectors where similar meanings are close together.",
    "FAISS is a library for fast similarity search and clustering of dense vectors.",
    "Chunking splits long documents into smaller pieces for better retrieval accuracy.",
]

def embed(texts: list[str]) -> np.ndarray:
    return MODEL.encode(texts, convert_to_numpy=True)

if __name__ == "__main__":
    doc_vecs = embed(DOCUMENTS)

    index = faiss.IndexFlatIP(doc_vecs.shape[1])
    faiss.normalize_L2(doc_vecs)
    index.add(doc_vecs)

    query = "How do you find relevant documents?"
    q_vec = embed([query])
    faiss.normalize_L2(q_vec)

    scores, indices = index.search(q_vec, 3)

    print(f"Query: {query}\n")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. (score: {scores[0][i]:.3f}) {DOCUMENTS[idx]}")
