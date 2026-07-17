"""Reasoning patterns — chain-of-thought and reflection."""

import json
import re
from providers import get_provider


def chain_of_thought(question: str, provider: str = "ollama") -> dict:
    prompt = f"""{question}

Think step-by-step:
1. First, understand what the question is asking.
2. Break down the problem into parts.
3. Work through each part.
4. Combine the parts into a final answer.

Final answer:"""
    _, resp = __import__("router").route(
        prompt, preferred_provider=provider, temperature=0.3, system="You are a careful, step-by-step reasoner."
    )
    return {"question": question, "reasoning": resp.content, "provider": provider}


def reflect(question: str, provider: str = "ollama") -> dict:
    _, first = route(question, preferred_provider=provider, temperature=0.7)

    critique_prompt = f"""Review the following answer for errors, omissions, or unclear reasoning:

Question: {question}
Answer: {first.content}

List specific issues and suggest improvements."""
    _, critique = route(critique_prompt, preferred_provider=provider, temperature=0.3)

    revise_prompt = f"""Original question: {question}

First attempt: {first.content}

Critique: {critique.content}

Provide a revised, improved answer."""
    _, revised = route(revise_prompt, preferred_provider=provider, temperature=0.5)

    return {
        "question": question,
        "first_attempt": first.content,
        "critique": critique.content,
        "revised_answer": revised.content,
    }


def route(query, preferred_provider=None, temperature=0.7, max_tokens=1024, system=None):
    from router import route as _route
    return _route(query, preferred_provider, temperature, max_tokens, system)
