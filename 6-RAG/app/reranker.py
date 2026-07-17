"""Cross-encoder reranker for improving retrieval quality."""

from typing import List, Tuple

from sentence_transformers import CrossEncoder

_model = None


def _get_model(model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
    global _model
    if _model is None:
        _model = CrossEncoder(model_name)
    return _model


def rerank(query: str, candidates: List[Tuple[str, float]], top_k: int = 3) -> List[Tuple[str, float]]:
    if not candidates:
        return []
    model = _get_model()
    pairs = [(query, chunk) for chunk, _ in candidates]
    scores = model.predict(pairs)
    ranked = sorted(zip([c for c, _ in candidates], scores), key=lambda x: x[1], reverse=True)
    return [(chunk, float(score)) for chunk, score in ranked[:top_k]]
