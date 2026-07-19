"""Chunking with sentence-aware splitting and metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Chunk:
    text: str
    source: str = ""
    section: str = ""
    metadata: dict = field(default_factory=dict)


def chunk_text(
    text: str,
    source: str = "",
    chunk_size: int = 80,
    overlap: int = 20,
) -> List[Chunk]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: List[Chunk] = []
    current_words: List[str] = []
    word_count = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        if word_count + len(sentence_words) > chunk_size and current_words:
            chunks.append(Chunk(
                text=" ".join(current_words),
                source=source,
            ))
            overlap_words = current_words[-overlap:] if overlap > 0 else []
            current_words = list(overlap_words)
            word_count = len(overlap_words)
        current_words.extend(sentence_words)
        word_count += len(sentence_words)

    if current_words:
        chunks.append(Chunk(
            text=" ".join(current_words),
            source=source,
        ))
    return chunks
