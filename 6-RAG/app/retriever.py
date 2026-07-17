"""Semantic retriever using sentence-transformers + FAISS."""

from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

_model = None
_index = None
_chunks: List[str] = []


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def build_index(chunks: List[str]):
    global _index, _chunks
    _chunks = chunks
    if not chunks:
        _index = None
        return
    model = _get_model()
    embeddings = model.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    _index.add(embeddings)


def retrieve_relevant_chunks(query: str, chunks: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    if _index is None or _chunks is not chunks:
        build_index(chunks)
    model = _get_model()
    q_vec = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_vec)
    scores, indices = _index.search(q_vec, min(top_k, len(_chunks)))
    return [(_chunks[i], float(scores[0][j])) for j, i in enumerate(indices[0])]
