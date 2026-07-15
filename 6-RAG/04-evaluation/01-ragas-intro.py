"""Phase 6 - Evaluation basics for RAG.

This file introduces the idea of evaluating retrieved results and generated answers.
Real RAG evaluation often uses metrics like faithfulness, relevance, and precision.
"""


def evaluate_answer(question: str, answer: str, context: str):
    faithfulness = "supported" if answer.lower() in context.lower() or context.lower() in answer.lower() else "not clearly supported"
    relevance = "relevant" if question.lower() in answer.lower() or len(answer.split()) > 3 else "needs review"

    return {
        "question": question,
        "answer": answer,
        "faithfulness": faithfulness,
        "relevance": relevance,
    }


if __name__ == "__main__":
    result = evaluate_answer(
        "What is RAG?",
        "RAG is retrieval-augmented generation.",
        "RAG uses retrieval to provide context before generation."
    )
    print(result)
