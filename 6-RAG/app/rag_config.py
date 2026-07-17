"""Configuration for the Phase 6 RAG project."""

DATA_DIR = "data/raw/sample_docs"
CHUNK_DIR = "data/processed/chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_TOP_K = 3
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
