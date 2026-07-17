"""Phase 6 — RAG evaluation with the ragas library.

Measures faithfulness, answer relevancy, and context precision
using ragas metrics. Run against a small set of test queries.
"""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision


def run_ragas_evaluation(questions, answers, contexts):
    data = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    })
    result = evaluate(data, metrics=[faithfulness, answer_relevancy, context_precision])
    print(result)
    return result


if __name__ == "__main__":
    demo = run_ragas_evaluation(
        questions=["What is RAG?"],
        answers=["RAG is retrieval-augmented generation."],
        contexts=[["RAG uses retrieval to provide context before generation."]],
    )
    print(demo)
