"""Configuration for the Research Agent project.

Indexes Notes/ markdown files into ChromaDB and
uses LangGraph + Ollama (or HF Inference API) to answer
conceptual AI Engineering questions.
"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

REPO_ROOT = PROJECT_DIR.parent.parent
NOTES_DIR = REPO_ROOT / "Notes"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

TOP_K_RETRIEVAL = 6

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama2")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

MAX_REVISIONS = 2
