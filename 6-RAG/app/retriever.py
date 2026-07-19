"""Semantic retriever using sentence-transformers + FAISS with metadata filtering."""

from __future__ import annotations

from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.chunker import Chunk
from app.rag_config import EMBEDDING_MODEL, EMBEDDING_MODEL_OPTIONS, EMBEDDING_MODEL_PROFILE

_model: SentenceTransformer | None = None
_index: faiss.Index | None = None
_chunks: List[Chunk] = []


def _resolve_model_name() -> str:
    return EMBEDDING_MODEL_OPTIONS.get(EMBEDDING_MODEL_PROFILE, EMBEDDING_MODEL)


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        model_name = _resolve_model_name()
        _model = SentenceTransformer(model_name)
    return _model


def reset_model(profile: str | None = None) -> None:
    global _model, _index, _chunks
    _model = None
    _index = None
    _chunks = []
    if profile:
        from app.rag_config import EMBEDDING_MODEL_OPTIONS
        globals()["EMBEDDING_MODEL_PROFILE"] = profile
        _resolve_model_name()


def build_index(chunks: List[Chunk]) -> None:
    global _index, _chunks
    _chunks = chunks
    if not chunks:
        _index = None
        return
    model = _get_model()
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    _index.add(embeddings)


def retrieve_relevant_chunks(
    query: str,
    chunks: List[Chunk],
    top_k: int = 3,
    metadata_filter: dict | None = None,
) -> List[Tuple[Chunk, float]]:
    if _index is None or _chunks is not chunks:
        build_index(chunks)

    model = _get_model()
    q_vec = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_vec)

    search_k = min(top_k * 3, len(_chunks)) if metadata_filter else min(top_k, len(_chunks))
    scores, indices = _index.search(q_vec, max(search_k, 1))

    results: List[Tuple[Chunk, float]] = []
    for j, i in enumerate(indices[0]):
        if i < 0 or i >= len(_chunks):
            continue
        chunk = _chunks[i]
        if metadata_filter and not _matches_filter(chunk, metadata_filter):
            continue
        results.append((chunk, float(scores[0][j])))
        if len(results) >= top_k:
            break

    return results


def _matches_filter(chunk: Chunk, metadata_filter: dict) -> bool:
    for key, value in metadata_filter.items():
        if key == "source":
            if chunk.source != value:
                return False
        elif key in chunk.metadata:
            if chunk.metadata[key] != value:
                return False
        else:
            return False
    return True
