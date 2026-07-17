"""End-to-end RAG pipeline with real embeddings and LLM call."""

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.retriever import retrieve_relevant_chunks
from app.rag_config import DATA_DIR
from app.ollama_client import generate_with_ollama


def ask(question: str, top_k: int = 3, model: str = "llama2") -> dict:
    raw_documents = load_text_files(DATA_DIR)
    chunks = []
    for doc in raw_documents:
        chunks.extend(chunk_text(doc))

    retrieved = retrieve_relevant_chunks(question, chunks, top_k=top_k)
    context_chunks = [chunk for chunk, _ in retrieved]
    scores = [score for _, score in retrieved]
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}
"""
    answer = generate_with_ollama(prompt, model=model)
    return {
        "question": question,
        "context": context_chunks,
        "scores": scores,
        "answer": answer,
    }


if __name__ == "__main__":
    result = ask("What is chunking and why does it matter?")
    print(f"Q: {result['question']}")
    print(f"A: {result['answer']}")
