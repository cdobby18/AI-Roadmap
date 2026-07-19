"""Configuration for the Phase 6 RAG project."""

from typing import Literal

DATA_DIR = "data/raw/sample_docs"
CHUNK_DIR = "data/processed/chunks"
DEFAULT_TOP_K = 3
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Embedding model — swap via config, no code changes needed
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_MODEL_OPTIONS = {
    "fast": "sentence-transformers/all-MiniLM-L6-v2",       # 384d, CPU-friendly
    "balanced": "BAAI/bge-small-en-v1.5",                   # 384d, better quality
    "quality": "BAAI/bge-large-en-v1.5",                    # 1024d, needs more compute
    "best": "intfloat/e5-mistral-7b-instruct",               # 4096d, GPU required
}
EMBEDDING_MODEL_PROFILE: Literal["fast", "balanced", "quality", "best"] = "fast"

# Chunking
CHUNK_SIZE = 80
CHUNK_OVERLAP = 20

# Query rewriting
REWRITER_STRATEGY = "standalone"  # "none" | "standalone" | "hyde" | "both"
REWRITER_MODEL = "llama2"
REWRITER_TEMPERATURE = 0.3
