"""Phase 6 - Conversational RAG.

Real chat systems keep previous user turns so the answer can be grounded in both
current and recent context.
"""


def build_conversation_prompt(history: list[str], latest_question: str, context: str) -> str:
    history_text = "\n".join(history)
    return f"""You are a conversational assistant.
Use the conversation history and the retrieved context to answer the latest question.

Conversation history:
{history_text}

Retrieved context:
{context}

Latest question:
{latest_question}"""


if __name__ == "__main__":
    history = [
        "User: What is RAG?",
        "Assistant: RAG is retrieval-augmented generation.",
    ]
    print(build_conversation_prompt(history, "Can you give me a simple example?", "RAG adds retrieved context before generation."))
