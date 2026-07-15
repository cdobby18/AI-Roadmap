"""Phase 6 - Prompt design for RAG.

A good RAG prompt should instruct the model to:
- use the provided context
- say when context is insufficient
- avoid hallucinating
"""


def build_rag_prompt(question: str, context: str) -> str:
    return f"""You are a helpful assistant.
Use the context below to answer the user's question.
If the context does not contain the answer, say you do not know.
Do not invent facts.

Context:
{context}

Question:
{question}"""


if __name__ == "__main__":
    context = "RAG uses retrieval to bring relevant information into the prompt."
    question = "What is RAG?"
    print(build_rag_prompt(question, context))
