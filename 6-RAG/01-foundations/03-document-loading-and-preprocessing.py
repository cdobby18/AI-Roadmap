"""Phase 6 - Document loading and preprocessing.

Real RAG systems often work with multiple file formats and need basic cleanup.
This example shows how to load text and normalize it before chunking.
"""

from pathlib import Path


def clean_text(text: str) -> str:
    return " ".join(text.lower().split())


def load_text_documents(folder: str):
    paths = sorted(Path(folder).glob("*.txt"))
    docs = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        docs.append(clean_text(raw))
    return docs


if __name__ == "__main__":
    docs = load_text_documents("data/raw/sample_docs")
    for doc in docs:
        print(doc[:200])
        print("---")
