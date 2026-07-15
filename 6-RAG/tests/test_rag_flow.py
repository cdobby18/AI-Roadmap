"""Simple sanity checks for the RAG project structure."""

from pathlib import Path


def test_sample_data_exists():
    assert Path("data/raw/sample_docs/sample.txt").exists()


def test_config_module_imports():
    from app.rag_config import DATA_DIR
    assert DATA_DIR == "data/raw/sample_docs"
