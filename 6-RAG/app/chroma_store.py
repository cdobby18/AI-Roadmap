"""ChromaDB-backed vector store for the RAG app.

Usage:
    from app.chroma_store import index_documents, query_chroma

    index_documents(chunks)              # one-time setup
    results = query_chroma("question")   # returns [(chunk, score), ...]
"""

from typing import List, Tuple
import chromadb
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
CHROMA_PATH = "./chroma_app_data"
COLLECTION_NAME = "rag_app"

_collection = None

def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection

def _embed(texts: List[str]) -> List[List[float]]:
    return MODEL.encode(texts, convert_to_numpy=True).tolist()

def index_documents(chunks: List[str]):
    collection = _get_collection()
    collection.add(
        documents=chunks,
        embeddings=_embed(chunks),
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

def query_chroma(question: str, top_k: int = 3) -> List[Tuple[str, float]]:
    collection = _get_collection()
    results = collection.query(
        query_embeddings=_embed([question]),
        n_results=top_k,
    )
    if not results["documents"]:
        return []
    return list(zip(results["documents"][0], results["distances"][0]))
