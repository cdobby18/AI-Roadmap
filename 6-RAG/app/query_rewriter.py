"""Query rewriting module for production RAG.

Transforms user queries before retrieval to improve result quality.
Strategies:
  - standalone:   Rewrites context-dependent queries into self-contained form
  - hyde:         Generates a hypothetical answer document, embeds it for retrieval
"""

from __future__ import annotations

from typing import Callable, Literal

import numpy as np
from sentence_transformers import SentenceTransformer

from app.rag_config import REWRITER_MODEL, REWRITER_TEMPERATURE
from app.ollama_client import generate_with_ollama

Strategy = Literal["none", "standalone", "hyde", "both"]


class QueryRewriter:
    def __init__(
        self,
        strategy: Strategy = "standalone",
        llm_model: str = REWRITER_MODEL,
        embed_model: SentenceTransformer | None = None,
    ):
        self.strategy = strategy
        self.llm_model = llm_model
        self.embed_model = embed_model

    @classmethod
    def from_config(cls, embed_model: SentenceTransformer | None = None) -> "QueryRewriter":
        from app.rag_config import REWRITER_STRATEGY, REWRITER_MODEL
        return cls(strategy=REWRITER_STRATEGY, llm_model=REWRITER_MODEL, embed_model=embed_model)

    def rewrite(self, question: str, history: list[str] | None = None) -> str:
        if self.strategy == "none":
            return question
        return self._rewrite_standalone(question, history)

    def rewrite_and_embed(
        self,
        question: str,
        chunks: list[str],
        history: list[str] | None = None,
    ) -> tuple[np.ndarray, str]:
        standalone = self._rewrite_standalone(question, history)

        if self.strategy in ("hyde", "both"):
            hypo_doc = self._generate_hypothetical(standalone)
            embedding = self.embed_model.encode(hypo_doc, convert_to_numpy=True)
            return embedding, standalone

        embedding = self.embed_model.encode(standalone, convert_to_numpy=True)
        return embedding, standalone

    def _rewrite_standalone(self, question: str, history: list[str] | None) -> str:
        if not history:
            return question

        history_text = "\n".join(history[-4:])
        prompt = f"""You are a query rewriter for a RAG system.
Rewrite the user's latest question as a standalone, self-contained search query.
If the question is already standalone, return it unchanged.

Conversation history:
{history_text}

Latest question: {question}

Rewritten standalone query:"""

        rewritten = generate_with_ollama(prompt, model=self.llm_model).strip()
        return rewritten if rewritten else question

    def _generate_hypothetical(self, question: str) -> str:
        prompt = f"""You are a document generator for a RAG system.
Given a question, write a short paragraph that would be the ideal retrieved chunk
to answer it. Write factual, informative text as if from a real document.

Question: {question}

Hypothetical document:"""

        hypo = generate_with_ollama(
            prompt,
            model=self.llm_model,
        ).strip()
        return hypo if hypo else question

    def rewrite_batch(
        self,
        questions: list[str],
        histories: list[list[str]] | None = None,
    ) -> list[str]:
        if histories is None:
            histories = [None] * len(questions)
        return [self.rewrite(q, h) for q, h in zip(questions, histories)]


def make_rewriter(
    strategy: Strategy = "standalone",
    embed_model: SentenceTransformer | None = None,
) -> QueryRewriter:
    return QueryRewriter(strategy=strategy, embed_model=embed_model)
