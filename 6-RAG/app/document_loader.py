"""Utilities for loading documents from the data folder."""

from pathlib import Path
from typing import List, Tuple


def load_text_files(folder: str) -> List[Tuple[str, str]]:
    """Read all .txt files from a folder. Returns [(filename, content), ...]."""
    files = sorted(Path(folder).glob("*.txt"))
    documents: List[Tuple[str, str]] = []
    for path in files:
        documents.append((path.name, path.read_text(encoding="utf-8")))
    return documents
