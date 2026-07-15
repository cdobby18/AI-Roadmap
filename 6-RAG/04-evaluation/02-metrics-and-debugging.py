"""Phase 6 - RAG evaluation metrics and debugging.

This file introduces common evaluation ideas used in RAG systems:
- faithfulness
- answer relevance
- context precision
- retrieval debugging
"""


def evaluate_rag(question: str, answer: str, retrieved_context: str):
    faithfulness = "faithful" if answer.lower() in retrieved_context.lower() or retrieved_context.lower() in answer.lower() else "needs review"
    relevance = "relevant" if question.lower() in answer.lower() or len(answer.split()) > 5 else "needs review"
    context_precision = "good" if len(retrieved_context.split()) > 10 else "thin"

    return {
        "faithfulness": faithfulness,
        "answer_relevance": relevance,
        "context_precision": context_precision,
    }


if __name__ == "__main__":
    result = evaluate_rag(
        "What is RAG?",
        "RAG is retrieval-augmented generation.",
        "RAG uses retrieved context before generating an answer."
    )
    print(result)
