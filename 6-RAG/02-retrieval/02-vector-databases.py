"""Phase 6 - Vector databases with ChromaDB.

What makes a vector DB different from FAISS:
- Data persists to disk (survives restarts)
- Can add/remove documents without rebuilding the whole index
- Built-in metadata filtering
- Client-server or in-process (ChromaDB does both)
"""

import chromadb
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts: list[str]) -> list[list[float]]:
    return MODEL.encode(texts, convert_to_numpy=True).tolist()

DOCUMENTS = [
    "RAG stands for Retrieval-Augmented Generation. It retrieves relevant documents before generating an answer.",
    "Chunking splits documents into smaller pieces so retrieval can find the exact relevant section.",
    "Embeddings convert text into numerical vectors. Similar texts have similar vectors.",
    "Vector databases store embeddings and support fast similarity search at scale.",
    "FAISS is a vector index library. It is fast but does not persist to disk by default.",
    "ChromaDB is a vector database. It persists data, supports metadata filtering, and has a simple API.",
]

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_data")
    collection = client.get_or_create_collection("rag_demo")

    collection.add(
        documents=DOCUMENTS,
        embeddings=embed(DOCUMENTS),
        ids=[f"doc_{i}" for i in range(len(DOCUMENTS))],
    )

    query = "What is a vector database?"
    results = collection.query(
        query_embeddings=embed([query]),
        n_results=2,
    )

    print(f"Query: {query}\n")
    for i, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0])):
        print(f"{i+1}. (distance: {dist:.3f}) {doc}")

    print("\n--- Data persists across runs ---")
    print(f"Collection has {collection.count()} documents")
