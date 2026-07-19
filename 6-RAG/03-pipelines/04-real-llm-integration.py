"""Phase 6 - Final integration step: connect retrieval to a real LLM.

This example shows the last step of a RAG system:
1. load documents
2. split them into chunks
3. retrieve the most relevant chunks
4. build a prompt with that context
5. call an LLM with the prompt

Note:
- This example uses the OpenAI-compatible API pattern so it is easy to adapt
  to Ollama, OpenAI, or other local providers.
- It is intentionally simple and educational rather than production-ready.
"""

import os
from typing import List

import requests

from app.chunker import chunk_text
from app.document_loader import load_text_files
from app.retriever import retrieve_relevant_chunks
from app.rag_config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def build_prompt(question: str, context_chunks: List[str]) -> str:
    context = "\n\n".join(context_chunks)
    return f"""Use the context below to answer the question.
If the answer is not present, say that you do not know.

Context:
{context}

Question:
{question}
"""


def call_llm(prompt: str, model: str = "llama2") -> str:
    """Call a local Ollama server if available."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.RequestException as exc:
        return f"LLM call failed: {exc}. Make sure Ollama is running and the model is installed."


def run_rag_with_llm(question: str, model: str = "llama2") -> str:
    documents = load_text_files(DATA_DIR)
    chunks = []
    for source, content in documents:
        chunks.extend(chunk_text(content, source=source, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP))

    retrieved = retrieve_relevant_chunks(question, chunks, top_k=3)
    context_chunks = [c.text for c, _ in retrieved]
    prompt = build_prompt(question, context_chunks)
    return call_llm(prompt, model=model)


if __name__ == "__main__":
    question = "What is RAG?"
    answer = run_rag_with_llm(question)
    print("Question:", question)
    print("Answer:")
    print(answer)