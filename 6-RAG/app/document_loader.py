"""Utilities for loading documents from the data folder."""

from pathlib import Path


def load_text_files(folder: str):
    """Read all .txt files from a folder and return their contents."""
    files = sorted(Path(folder).glob("*.txt"))
    documents = []
    for path in files:
        documents.append(path.read_text(encoding="utf-8"))
    return documents
