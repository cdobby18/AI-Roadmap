"""Sanity checks for the RAG project."""

from pathlib import Path


def test_sample_data_exists():
    data_dir = Path("data/raw/sample_docs")
    assert data_dir.exists()
    txt_files = list(data_dir.glob("*.txt"))
    assert len(txt_files) >= 3


def test_config_module_imports():
    from app.rag_config import DATA_DIR, EMBEDDING_MODEL_OPTIONS, EMBEDDING_MODEL_PROFILE
    assert DATA_DIR == "data/raw/sample_docs"
    assert "fast" in EMBEDDING_MODEL_OPTIONS
    assert EMBEDDING_MODEL_PROFILE in EMBEDDING_MODEL_OPTIONS


def test_chunker_splits():
    from app.chunker import chunk_text
    text = "First sentence about RAG. Second sentence about chunking. Third sentence about embeddings."
    chunks = chunk_text(text, source="test.txt", chunk_size=10, overlap=2)
    assert len(chunks) >= 1
    assert all(c.text for c in chunks)
    assert all(c.source == "test.txt" for c in chunks)


def test_chunk_dataclass():
    from app.chunker import Chunk
    c = Chunk(text="hello", source="doc.txt", section="intro")
    assert c.text == "hello"
    assert c.source == "doc.txt"
    assert c.metadata == {}


def test_retriever_imports():
    from app.retriever import retrieve_relevant_chunks, reset_model
    import faiss
    from sentence_transformers import SentenceTransformer
    assert callable(retrieve_relevant_chunks)
    assert callable(reset_model)


def test_pipeline_builds_prompt():
    from app.rag_pipeline import ask
    result = ask("What is RAG?", top_k=1)
    assert "question" in result
    assert "answer" in result
    assert "context" in result
    assert "sources" in result
