"""Phase 6 - Chunking strategies for RAG.

Chunking is one of the most important parts of RAG because the quality of
retrieval depends heavily on how documents are split.
"""

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


if __name__ == "__main__":
    sample_text = (
        "RAG combines retrieval with generation. "
        "It helps language models answer questions using external context. "
        "Good chunking improves retrieval quality and reduces noise."
    )

    print(chunk_text(sample_text, chunk_size=10, overlap=3))
