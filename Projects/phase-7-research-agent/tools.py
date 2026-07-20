"""Tool registry for the Research Agent.

Defines tools the agent can use during research:
  1. search_knowledge_base — Vector search over indexed Notes/ files
  2. search_by_category   — Narrow search within phases, reference, or projects

Follows LangChain's @tool convention so the agent can
discover and invoke tools by name + description.
"""

from typing import Optional

from langchain_core.tools import tool

from knowledge_base import search_notes as kb_search


@tool
def search_knowledge_base(query: str, top_k: int = 5) -> str:
    """Search the AI Engineering Roadmap knowledge base for relevant information.

    The knowledge base contains markdown notes covering:
    - Phase 1-8 concepts (Python, FastAPI, ML, NLP, LLMs, RAG, Advanced Frameworks, Deploy)
    - System design patterns
    - AI concepts (embeddings, vector DBs, RAG, MCP, agents, LangChain, LangGraph)
    - Project documentation and lessons learned
    - Mentorship feedback

    Use this tool when you need to find specific information about
    AI Engineering concepts, compare approaches, or understand tradeoffs.

    Args:
        query: The search query — be specific (e.g., "RAG vs fine-tuning tradeoffs")
        top_k: Number of results to return (default 5, max 10)

    Returns:
        Formatted string with top matching chunks and their sources.
    """
    results = kb_search(query, top_k=min(top_k, 10))
    if not results:
        return "No relevant information found in the knowledge base."

    output = []
    for i, r in enumerate(results, 1):
        output.append(f"[Result {i}] (score: {r['score']}) — {r['source']}")
        output.append(f"Category: {r['category']}")
        output.append(r["text"][:500])
        output.append("")
    return "\n".join(output)


@tool
def search_by_category(query: str, category: str, top_k: int = 3) -> str:
    """Search within a specific category of notes.

    Categories:
      - phases: Phase summary notes (phase-1.md through phase-8.md, system-design-patterns.md)
      - reference: AI concepts overview and mentorship feedback
      - projects: Project context and lessons learned for all 6 projects

    Use this when you need information from a specific part of the roadmap.

    Args:
        query: The search query
        category: One of: phases, reference, projects
        top_k: Number of results (default 3)

    Returns:
        Formatted string with matching chunks from the specified category.
    """
    valid = {"phases", "reference", "projects"}
    if category not in valid:
        return f"Invalid category '{category}'. Choose from: {', '.join(sorted(valid))}"

    results = kb_search(query, top_k=min(top_k, 5), category=category)
    if not results:
        return f"No results found in '{category}' for: {query}"

    output = []
    for i, r in enumerate(results, 1):
        output.append(f"[Result {i}] (score: {r['score']}) — {r['source']}")
        output.append(r["text"][:400])
        output.append("")
    return "\n".join(output)


TOOLS = [search_knowledge_base, search_by_category]
TOOL_NAMES = {t.name for t in TOOLS}
