"""Smart provider routing — picks the best provider for each query."""

import re
from typing import Optional

from providers import LLMResponse, get_provider


def route(
    query: str,
    preferred_provider: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    system: Optional[str] = None,
) -> tuple[str, LLMResponse]:
    """Route a query to the best provider. Returns (provider_name, response)."""
    if preferred_provider and preferred_provider != "auto":
        provider = get_provider(preferred_provider)
        return preferred_provider, provider.generate(
            query, system=system, temperature=temperature, max_tokens=max_tokens
        )

    needs_tools = bool(re.search(r"\b(calculate|weather|search|compute)\b", query, re.IGNORECASE))
    needs_cheap = bool(re.search(r"\b(summarize|translate|rephrase|extract)\b", query, re.IGNORECASE))

    if needs_tools:
        name = "openai"
    elif needs_cheap:
        name = "ollama"
    else:
        name = "ollama"

    provider = get_provider(name)
    return name, provider.generate(
        query, system=system, temperature=temperature, max_tokens=max_tokens
    )
