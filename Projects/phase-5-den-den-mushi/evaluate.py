"""Benchmark runner — scores the system against a test set."""

import json
import time
from pathlib import Path
from dataclasses import dataclass, field

from providers import get_provider


@dataclass
class TestCase:
    query: str
    expected_keywords: list[str] = field(default_factory=list)
    min_length: int = 1
    expected_provider: str = "ollama"


TEST_SET = [
    TestCase("What is 2 + 2?", expected_keywords=["4"], min_length=1, expected_provider="ollama"),
    TestCase("Summarize: RAG is retrieval augmented generation.", expected_keywords=["retrieval", "generation"], min_length=10),
    TestCase("Translate hello to Spanish.", expected_keywords=["hola"], min_length=1),
    TestCase("Extract numbers from 'I have 3 apples and 5 oranges'", expected_keywords=["3", "5"], min_length=5),
]


def score_response(response: str, test: TestCase) -> dict:
    keywords_found = [kw for kw in test.expected_keywords if kw.lower() in response.lower()]
    length_ok = len(response.split()) >= test.min_length
    return {
        "keyword_coverage": len(keywords_found) / max(len(test.expected_keywords), 1),
        "keywords_found": keywords_found,
        "length_ok": length_ok,
        "response_length": len(response.split()),
    }


def run_benchmark(tests: list[TestCase] = None, provider: str = "ollama") -> dict:
    if tests is None:
        tests = TEST_SET
    results = []
    total_score = 0.0

    for test in tests:
        prov = get_provider(provider)
        start = time.time()
        resp = prov.generate(test.query)
        elapsed = time.time() - start
        scores = score_response(resp.content, test)
        passed = scores["keyword_coverage"] >= 0.5 and scores["length_ok"]
        if passed:
            total_score += 1.0

        results.append({
            "query": test.query,
            "response": resp.content[:200],
            "latency_s": round(elapsed, 2),
            "scores": scores,
            "passed": passed,
        })

    return {
        "total_tests": len(tests),
        "passed": sum(1 for r in results if r["passed"]),
        "pass_rate": round(total_score / max(len(tests), 1), 2),
        "avg_latency_s": round(sum(r["latency_s"] for r in results) / max(len(results), 1), 2),
        "results": results,
    }


if __name__ == "__main__":
    result = run_benchmark()
    print(json.dumps(result, indent=2))
