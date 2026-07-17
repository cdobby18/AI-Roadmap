"""Phase 6 — RAG debugging toolkit.

Custom metrics for diagnosing where a RAG pipeline breaks.
Use these alongside ragas for deeper introspection.
"""


def diagnose_retrieval(question: str, chunks: list[str], scores: list[float]) -> dict:
    return {
        "question": question,
        "num_chunks_retrieved": len(chunks),
        "max_score": max(scores) if scores else 0.0,
        "min_score": min(scores) if scores else 0.0,
        "score_spread": max(scores) - min(scores) if len(scores) > 1 else 0.0,
        "low_confidence": any(s < 0.3 for s in scores),
    }


def diagnose_generation(answer: str, context_chunks: list[str]) -> dict:
    context = " ".join(context_chunks)
    answer_lower = answer.lower()
    context_lower = context.lower()
    supported_terms = sum(1 for term in answer_lower.split() if len(term) > 3 and term in context_lower)
    total_terms = sum(1 for t in answer_lower.split() if len(t) > 3)
    faithfulness_ratio = supported_terms / total_terms if total_terms > 0 else 0.0
    return {
        "answer_length": len(answer.split()),
        "faithfulness_ratio": round(faithfulness_ratio, 3),
        "hallucination_risk": faithfulness_ratio < 0.5,
    }


def full_diagnosis(question, answer, chunks, scores):
    return {
        "retrieval": diagnose_retrieval(question, chunks, scores),
        "generation": diagnose_generation(answer, chunks),
    }


if __name__ == "__main__":
    result = full_diagnosis(
        "What is RAG?",
        "RAG is retrieval-augmented generation.",
        ["RAG uses retrieval to provide context before generation."],
        [0.92],
    )
    print(result)
