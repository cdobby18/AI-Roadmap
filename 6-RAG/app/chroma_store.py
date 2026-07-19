"""ChromaDB-backed vector store for the RAG app.

Usage:
    from app.chroma_store import index_documents, query_chroma

    index_documents(chunks)              # one-time setup
    results = query_chroma("question")   # returns [(chunk, score), ...]
"""

from __future__ import annotations

from typing import List, Tuple

import chromadb
from sentence_transformers import SentenceTransformer

from app.chunker import Chunk
from app.rag_config import EMBEDDING_MODEL_OPTIONS, EMBEDDING_MODEL_PROFILE

CHROMA_PATH = "./chroma_app_data"
COLLECTION_NAME = "rag_app"

_model: SentenceTransformer | None = None
_collection = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        model_name = EMBEDDING_MODEL_OPTIONS.get(EMBEDDING_MODEL_PROFILE, EMBEDDING_MODEL_PROFILE)
        _model = SentenceTransformer(model_name)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def _embed(texts: List[str]) -> List[List[float]]:
    return _get_model().encode(texts, convert_to_numpy=True).tolist()


def index_documents(chunks: List[Chunk]):
    collection = _get_collection()
    texts = [c.text for c in chunks]
    metadatas = [{"source": c.source} for c in chunks]
    collection.add(
        documents=texts,
        embeddings=_embed(texts),
        metadatas=metadatas,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )


def query_chroma(
    question: str,
    top_k: int = 3,
    metadata_filter: dict | None = None,
) -> List[Tuple[str, float]]:
    collection = _get_collection()
    where = None
    if metadata_filter and "source" in metadata_filter:
        where = {"source": metadata_filter["source"]}

    results = collection.query(
        query_embeddings=_embed([question]),
        n_results=top_k,
        where=where,
    )
    if not results["documents"]:
        return []
    return list(zip(results["documents"][0], results["distances"][0]))
