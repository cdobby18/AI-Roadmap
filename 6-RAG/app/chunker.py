"""Chunking with sentence-aware splitting."""

import re
from typing import List


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 20) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current = []
    word_count = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        if word_count + len(sentence_words) > chunk_size and current:
            chunks.append(" ".join(current))
            overlap_words = current[-overlap:] if overlap > 0 else []
            current = list(overlap_words)
            word_count = len(overlap_words)
        current.extend(sentence_words)
        word_count += len(sentence_words)

    if current:
        chunks.append(" ".join(current))
    return chunks
