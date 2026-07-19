"""Document ingestion pipeline — scrape → chunk → embed → store in ChromaDB.

This is the ETL (Extract, Transform, Load) pipeline for RAG:
1. Extract: Scrape wiki pages (via scraper.py) or load existing text files
2. Transform: Split documents into overlapping chunks
3. Embed: Convert each chunk into a vector using sentence-transformers
4. Load: Store vectors + metadata in ChromaDB for fast similarity search

Why chunking matters:
- LLMs have context windows (typically 4K-8K tokens)
- A single wiki page can be 10K+ tokens
- Chunking preserves meaning while keeping each piece retrievable
- Overlap ensures no information is lost at chunk boundaries
"""

import re
from typing import List, Tuple

from sentence_transformers import SentenceTransformer
import chromadb

from config import CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


# -------------------------------------------------------------------
# Chunking
# -------------------------------------------------------------------

def chunk_text(text: str, source: str = "", categories: List[str] = None) -> List[dict]:
    """Split text into overlapping chunks at sentence boundaries.

    Why sentence-aware splitting?
    - Word-level splits can cut sentences in half, losing meaning
    - Sentence boundaries (. ! ?) are natural breakpoints
    - Overlap preserves context across chunk boundaries

    Each chunk is a dict with:
        text        — the chunk content
        source      — document identifier
        categories  — tags for metadata filtering
        chunk_id    — unique ID for dedup in vector DB
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current = []
    word_count = 0

    for sentence in sentences:
        words = sentence.split()
        if word_count + len(words) > CHUNK_SIZE and current:
            chunk_text_str = " ".join(current)
            chunks.append({
                "text": chunk_text_str,
                "source": source,
                "categories": categories or [],
                "chunk_id": f"{source}_{len(chunks)}",
            })
            # Overlap: keep last N words from previous chunk
            overlap_words = current[-CHUNK_OVERLAP:] if CHUNK_OVERLAP > 0 else []
            current = list(overlap_words)
            word_count = len(overlap_words)
        current.extend(words)
        word_count += len(words)

    if current:
        chunks.append({
            "text": " ".join(current),
            "source": source,
            "categories": categories or [],
            "chunk_id": f"{source}_{len(chunks)}",
        })
    return chunks


# -------------------------------------------------------------------
# Embedding model
# -------------------------------------------------------------------

_embed_model = None


def get_embed_model() -> SentenceTransformer:
    """Lazy-load the embedding model (loaded once, reused)."""
    global _embed_model
    if _embed_model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def embed(texts: List[str]) -> List[List[float]]:
    """Convert a list of text strings to embedding vectors."""
    model = get_embed_model()
    return model.encode(texts, convert_to_numpy=True).tolist()


# -------------------------------------------------------------------
# ChromaDB vector store
# -------------------------------------------------------------------

_chroma_client = None
_chroma_collection = None


def get_collection():
    """Lazy-load the ChromaDB collection (persistent across restarts)."""
    global _chroma_client, _chroma_collection
    if _chroma_collection is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _chroma_collection = _chroma_client.get_or_create_collection(
            "poneglyph_reader",
            metadata={"hnsw:space": "cosine"},
        )
    return _chroma_collection


def index_documents(documents: List[dict]) -> int:
    """Chunk and index a list of documents into ChromaDB.

    Args:
        documents: List of dicts with keys: title, text, source_url, categories

    Returns:
        Number of chunks indexed
    """
    collection = get_collection()
    all_chunks = []

    for doc in documents:
        title = doc.get("title", "unknown")
        text = doc.get("text", "")
        source_url = doc.get("source_url", "")
        categories = doc.get("categories", [])
        source = f"{title} ({source_url})"

        chunks = chunk_text(text, source=source, categories=categories)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("No chunks to index.")
        return 0

    # Batch add to ChromaDB
    texts = [c["text"] for c in all_chunks]
    ids = [c["chunk_id"] for c in all_chunks]
    metadatas = [
        {
            "source": c["source"],
            "categories": ",".join(c["categories"]),
        }
        for c in all_chunks
    ]

    collection.add(
        documents=texts,
        embeddings=embed(texts),
        metadatas=metadatas,
        ids=ids,
    )
    print(f"Indexed {len(all_chunks)} chunks from {len(documents)} documents")
    return len(all_chunks)


def collection_stats() -> dict:
    """Return statistics about the indexed collection."""
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return {"count": 0, "sources": []}

    # Get unique sources via metadata
    results = collection.get(limit=count)
    sources = set()
    for meta in results.get("metadatas", []):
        if meta and "source" in meta:
            sources.add(meta["source"])
    return {
        "count": count,
        "sources": sorted(sources),
        "source_count": len(sources),
    }


def clear_collection():
    """Delete all documents from the collection."""
    collection = get_collection()
    count = collection.count()
    if count > 0:
        collection.delete(where={})
    print(f"Cleared {count} chunks from collection")


if __name__ == "__main__":
    from scraper import scrape_pages
    docs = scrape_pages()
    if docs:
        n = index_documents(docs)
        stats = collection_stats()
        print(f"\nCollection stats: {stats}")
