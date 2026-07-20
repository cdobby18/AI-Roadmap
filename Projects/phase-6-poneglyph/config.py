"""Configuration for the Poneglyph Reader RAG project.

Supports two LLM backends:
- ollama       — default for local development (requires Ollama on localhost:11434)
- hf_inference — for HuggingFace Spaces (uses HF Inference API, set HF_TOKEN for higher rate limits)
"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
CACHE_DIR = DATA_DIR / "cache"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 200
CHUNK_OVERLAP = 40

TOP_K_RETRIEVAL = 5
TOP_K_RERANK = 3

# --- LLM backend ---
# Auto-detect: HF Spaces sets SPACES=true
ON_HF_SPACES = os.getenv("SPACES", "").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hf_inference" if ON_HF_SPACES else "ollama")

# Ollama settings (used when LLM_PROVIDER == "ollama")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama2")

# HuggingFace Inference API settings (used when LLM_PROVIDER == "hf_inference")
HF_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")
HF_TOKEN = os.getenv("HF_TOKEN", "")

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

SCRAPER_DELAY = 1.0
WIKI_BASE_URL = "https://onepiece.fandom.com/wiki"

SEED_PAGES = [
    "Monkey_D._Luffy",
    "Roronoa_Zoro",
    "Nami",
    "Sanji",
    "Nico_Robin",
    "Tony_Tony_Chopper",
    "Franky",
    "Brook",
    "Jinbe",
    "Gol_D._Roger",
    "Shanks",
    "Whitebeard",
    "Gomu_Gomu_no_Mi",
    "Devil_Fruit",
    "Haki",
    "Grand_Line",
    "Red_Line",
    "Calm_Belt",
]
