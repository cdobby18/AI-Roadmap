"""Knowledge base — indexes Notes/ markdown files into ChromaDB.

Sources indexed:
  - Notes/phases/     (phase summary notes for each phase)
  - Notes/reference/  (concepts, mentorship feedback)
  - Notes/projects/   (project context and lessons)

Each document is chunked, embedded with sentence-transformers,
and stored in a persistent ChromaDB collection.
"""

import os
import re
from pathlib import Path
from typing import List, Optional

from sentence_transformers import SentenceTransformer
import chromadb

from config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    NOTES_DIR,
)


# -------------------------------------------------------------------
# Chunking
# -------------------------------------------------------------------

def chunk_markdown(text: str, source: str) -> List[dict]:
    """Split markdown text into overlapping chunks at sentence boundaries.

    Respects markdown structure: prefers splitting at ## headings
    before falling back to sentence boundaries.
    """
    chunks = []
    # Try splitting by ## sections first
    sections = re.split(r"\n(?=##\s)", text.strip())
    for section in sections:
        sentences = re.split(r"(?<=[.!?])\s+", section.strip())
        current = []
        word_count = 0
        for sentence in sentences:
            words = sentence.split()
            if word_count + len(words) > CHUNK_SIZE and current:
                chunk_text = " ".join(current)
                chunks.append({
                    "text": chunk_text,
                    "source": source,
                    "chunk_id": f"{source}_{len(chunks)}",
                })
                overlap_words = current[-CHUNK_OVERLAP:] if CHUNK_OVERLAP > 0 else []
                current = list(overlap_words)
                word_count = len(overlap_words)
            current.extend(words)
            word_count += len(words)
        if current:
            chunks.append({
                "text": " ".join(current),
                "source": source,
                "chunk_id": f"{source}_{len(chunks)}",
            })
    return chunks


# -------------------------------------------------------------------
# Document loader
# -------------------------------------------------------------------

def load_notes() -> List[dict]:
    """Load all markdown files from Notes/ into document dicts.

    Returns:
        List of dicts with keys: title, text, source_path, category
    """
    documents = []
    for root, _dirs, files in os.walk(str(NOTES_DIR)):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = Path(root) / fname
            rel_path = fpath.relative_to(NOTES_DIR.parent)
            text = fpath.read_text(encoding="utf-8")
            category = Path(root).name  # phases, reference, projects
            documents.append({
                "title": fname.replace(".md", ""),
                "text": text,
                "source_path": str(rel_path),
                "category": category,
            })
    return documents


# -------------------------------------------------------------------
# Embedding model
# -------------------------------------------------------------------

_embed_model: Optional[SentenceTransformer] = None


def get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def embed(texts: List[str]) -> List[List[float]]:
    model = get_embed_model()
    return model.encode(texts, convert_to_numpy=True).tolist()


# -------------------------------------------------------------------
# ChromaDB store
# -------------------------------------------------------------------

_chroma_client: Optional[chromadb.PersistentClient] = None
_chroma_collection = None


def get_collection():
    global _chroma_client, _chroma_collection
    if _chroma_collection is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _chroma_collection = _chroma_client.get_or_create_collection(
            "research_notes",
            metadata={"hnsw:space": "cosine"},
        )
    return _chroma_collection


def index_notes() -> int:
    """Load, chunk, embed, and store all Notes/ markdown files."""
    collection = get_collection()
    docs = load_notes()
    all_chunks = []

    for doc in docs:
        source = f"{doc['title']} ({doc['source_path']})"
        chunks = chunk_markdown(doc["text"], source=source)
        for c in chunks:
            c["category"] = doc["category"]
        all_chunks.extend(chunks)

    if not all_chunks:
        return 0

    texts = [c["text"] for c in all_chunks]
    ids = [c["chunk_id"] for c in all_chunks]
    metadatas = [{"source": c["source"], "category": c.get("category", "")} for c in all_chunks]

    collection.add(
        documents=texts,
        embeddings=embed(texts),
        metadatas=metadatas,
        ids=ids,
    )
    return len(all_chunks)


def collection_stats() -> dict:
    """Return count and unique sources in the index."""
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return {"count": 0, "sources": []}
    results = collection.get(limit=count)
    sources = set()
    for meta in results.get("metadatas", []):
        if meta and "source" in meta:
            sources.add(meta["source"])
    return {"count": count, "sources": sorted(sources), "source_count": len(sources)}


def search_notes(query: str, top_k: int = 5, category: Optional[str] = None) -> List[dict]:
    """Search the indexed notes for chunks matching the query.

    Args:
        query: The search query string.
        top_k: Number of results to return.
        category: Optional filter — one of: phases, reference, projects.

    Returns:
        List of dicts: {text, source, score, category}
    """
    collection = get_collection()
    query_vec = embed([query])

    where = None
    if category:
        where = {"category": category}

    results = collection.query(
        query_embeddings=query_vec,
        n_results=top_k,
        where=where,
    )

    if not results or not results.get("documents"):
        return []

    chunks = []
    for i in range(len(results["documents"][0])):
        meta = results["metadatas"][0][i] if results.get("metadatas") else {}
        distance = results["distances"][0][i] if results.get("distances") else 0.0
        chunks.append({
            "text": results["documents"][0][i],
            "source": meta.get("source", ""),
            "score": round(1.0 - distance, 3),
            "category": meta.get("category", ""),
        })
    return chunks


def clear():
    """Drop all documents from the collection."""
    collection = get_collection()
    count = collection.count()
    if count > 0:
        collection.delete(where={})
    return count


# -------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        cleared = clear()
        print(f"Cleared {cleared} chunks")
    else:
        n = index_notes()
        stats = collection_stats()
        print(f"Indexed {n} chunks from {stats['source_count']} sources")
        print(f"Sources: {stats['source_count']} unique files")

        if n:
            query = "How does RAG work?"
            results = search_notes(query)
            print(f"\nSearch: '{query}'")
            for r in results[:3]:
                print(f"  [{r['score']}] {r['source']}")
                print(f"      {r['text'][:120]}...")
