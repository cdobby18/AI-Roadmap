"""A minimal end-to-end RAG pipeline example."""

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.retriever import retrieve_relevant_chunks
from app.rag_config import DATA_DIR


def build_prompt(question: str, top_k: int = 3) -> str:
    raw_documents = load_text_files(DATA_DIR)
    chunks = []
    for doc in raw_documents:
        chunks.extend(chunk_text(doc))

    results = retrieve_relevant_chunks(question, chunks, top_k=top_k)
    context = "\n\n".join(chunk for chunk, _ in results)

    return f"""You are a helpful assistant.
Use the context below to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}
"""


if __name__ == "__main__":
    prompt = build_prompt("What is RAG?")
    print(prompt)
