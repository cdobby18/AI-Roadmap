"""Simple chunking utilities for RAG."""

from typing import List


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 20) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
