"""Research Agent — LangGraph multi-agent research system.

Architecture (StateGraph):
```
route_question ──► search_knowledge_base ──► generate_answer
                                                   │
                                                   ▼
                                              critique_answer
                                              │          │
                                         good enough    needs revision
                                              │          │
                                              ▼          ▼
                                             END    search_knowledge_base (loop)
```

Key patterns demonstrated:
  - StateGraph with custom state schema
  - Conditional routing (route by complexity, critique by quality)
  - Reflection loop (generate → critique → revise, max 2 cycles)
  - Tool integration via LangChain @tool decorators
  - LangSmith tracing ready (set LANGSMITH_API_KEY to enable)
"""

import json
import os
from typing import Dict, List, Literal, Optional, TypedDict

import requests
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from config import LLM_MODEL, LLM_TEMPERATURE, MAX_REVISIONS, OLLAMA_BASE_URL
from tools import TOOLS, search_knowledge_base, search_by_category


# -------------------------------------------------------------------
# State schema
# -------------------------------------------------------------------

class ResearchState(TypedDict):
    question: str
    rewritten_query: str
    category_filter: Optional[str]
    search_results: str
    context: str
    answer: str
    revision_count: int
    max_revisions: int
    messages: List[BaseMessage]
    final: bool


# -------------------------------------------------------------------
# LLM helpers
# -------------------------------------------------------------------

def call_llm(system: str, prompt: str, temperature: float = LLM_TEMPERATURE) -> str:
    """Call Ollama with a system prompt and user prompt."""
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.RequestException as e:
        return f"[Ollama unavailable: {e}]"


def call_llm_json(system: str, prompt: str) -> dict:
    """Call Ollama and parse the response as JSON."""
    raw = call_llm(system, f"{prompt}\n\nRespond in JSON only.", temperature=0.0)
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return {"error": "Failed to parse LLM response as JSON", "raw": raw}


# -------------------------------------------------------------------
# Tool execution
# -------------------------------------------------------------------

def run_tool(name: str, args: dict) -> str:
    """Execute a registered tool by name with the given args."""
    for tool in TOOLS:
        if tool.name == name:
            return tool.invoke(args)
    return f"Unknown tool: {name}"


# -------------------------------------------------------------------
# Graph nodes
# -------------------------------------------------------------------

def route_question(state: ResearchState) -> Dict:
    """Classify the question and determine the search strategy.

    Returns a rewritten query and optionally a category filter.
    """
    question = state["question"]

    classification = call_llm_json(
        "You classify questions about AI Engineering into categories and rewrite them for search.",
        f"""Classify this question and rewrite it as a focused search query.

Question: {question}

Respond with JSON:
{{
    "rewritten_query": "concise search query (5-15 words)",
    "category": "phases" | "reference" | "projects" | "all",
    "complexity": "simple" | "complex",
    "reasoning": "one-sentence explanation"
}}

Guidelines:
- simple: definition, fact, single-concept ("What is RAG?", "Define embedding")
- complex: comparison, tradeoff, multi-step ("RAG vs fine-tuning", "design a RAG pipeline")
- category: phases for roadmap phase topics, reference for general concepts, all if unsure
"""
    )

    rewritten = classification.get("rewritten_query", question)
    category = classification.get("category", "all")
    complexity = classification.get("complexity", "complex")

    return {
        "rewritten_query": rewritten,
        "category_filter": None if category == "all" else category,
        "messages": [
            SystemMessage(content=f"Question classified as {complexity}, searching category: {category}"),
            HumanMessage(content=question),
        ],
    }


def search(state: ResearchState) -> Dict:
    """Search the knowledge base using both broad and category-specific queries.

    Performs parallel searches:
      1. Full knowledge base search with the rewritten query
      2. Category-specific search if a category was identified

    This demonstrates LangGraph's ability to parallelize tool calls
    (though here we execute sequentially and merge results).
    """
    query = state.get("rewritten_query") or state["question"]
    category = state.get("category_filter")

    results = []

    broad = run_tool("search_knowledge_base", {"query": query, "top_k": 5})
    results.append(f"=== Broad Search Results ===\n{broad}")

    if category:
        specific = run_tool("search_by_category", {"query": query, "category": category, "top_k": 3})
        if "No results" not in specific:
            results.append(f"\n=== Category: {category} ===\n{specific}")

    combined = "\n\n".join(results)
    return {"search_results": combined}


def generate(state: ResearchState) -> Dict:
    """Synthesize search results into a comprehensive answer.

    Formats the search results as context and calls the LLM to
    produce a well-structured answer with citations.
    """
    question = state["question"]
    search_text = state.get("search_results", "")
    revision = state.get("revision_count", 0)

    system = """You are an AI Engineering tutor. Answer the question using ONLY the search results provided.
Cite sources when you use specific information from them using [Source: filename].
If the search results don't contain enough information, say so clearly.
Be specific about tradeoffs, comparisons, and practical implications."""

    prompt = f"""Question: {question}

Search Results:
{search_text}

{"This is revision " + str(revision + 1) + ". Improve upon the previous answer." if revision > 0 else ""}

Provide a clear, structured answer. Include specific details, tradeoffs, and source citations."""
    # Skip initial placeholder system since we pass system differently
    answer = call_llm(system, prompt)

    context = f"Question: {question}\n\nSearch Results:\n{search_text}"

    return {"answer": answer, "context": context}


def critique(state: ResearchState) -> Dict:
    """Reflection loop: evaluate the answer and decide if it needs revision.

    The LLM acts as a judge, scoring the answer on:
      - Completeness: Does it fully answer the question?
      - Accuracy: Are facts correct based on search results?
      - Citations: Are sources properly cited?
      - Clarity: Is the answer well-structured?

    If score < 7 (out of 10) and revisions remain, the agent loops back to search.
    """
    question = state["question"]
    answer = state["answer"]
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", MAX_REVISIONS)

    evaluation = call_llm_json(
        "You evaluate answer quality. Be critical — only pass truly excellent answers.",
        f"""Evaluate this answer on a scale of 1-10.

Question: {question}

Answer:
{answer}

Respond with JSON:
{{
    "score": <1-10>,
    "passed": true/false,
    "weaknesses": ["list specific gaps"],
    "suggestions": ["how to improve"]
}}

Pass (score >= 7) if the answer fully addresses the question,
cites sources, and is accurate. Fail (score < 7) if it's vague,
missing key points, or lacks citations."""
    )

    score = evaluation.get("score", 5)
    passed = evaluation.get("passed", False)
    weaknesses = evaluation.get("weaknesses", [])
    suggestions = evaluation.get("suggestions", [])

    should_revise = not passed and revision_count < max_revisions

    msg = f"Critique: score={score}/10, passed={passed}, revisions={revision_count}/{max_revisions}"
    if weaknesses:
        msg += f"\nWeaknesses: {'; '.join(weaknesses)}"
    if should_revise:
        msg += "\n→ Revising"

    return {
        "revision_count": revision_count + 1 if should_revise else revision_count,
        "final": not should_revise,
        "messages": [HumanMessage(content=msg)],
    }


# -------------------------------------------------------------------
# Conditional edge routers
# -------------------------------------------------------------------

def should_continue(state: ResearchState) -> Literal["continue", "end"]:
    """After critique: continue revising or end."""
    if state.get("final", False):
        return "end"
    return "continue"


# -------------------------------------------------------------------
# Build the graph
# -------------------------------------------------------------------

def build_research_agent() -> StateGraph:
    """Construct the Research Agent StateGraph."""

    workflow = StateGraph(ResearchState)

    workflow.add_node("route_question", route_question)
    workflow.add_node("search", search)
    workflow.add_node("generate", generate)
    workflow.add_node("critique", critique)

    workflow.set_entry_point("route_question")

    workflow.add_edge("route_question", "search")
    workflow.add_edge("search", "generate")
    workflow.add_edge("generate", "critique")

    workflow.add_conditional_edges(
        "critique",
        should_continue,
        {
            "continue": "search",
            "end": END,
        },
    )

    return workflow.compile()


# -------------------------------------------------------------------
# High-level interface
# -------------------------------------------------------------------

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = build_research_agent()
    return _agent


def research(question: str) -> dict:
    """Run the research agent on a question.

    Args:
        question: The question to research.

    Returns:
        Dict with keys: question, answer, revision_count, context, search_results
    """
    agent = get_agent()
    initial_state: ResearchState = {
        "question": question,
        "rewritten_query": "",
        "category_filter": None,
        "search_results": "",
        "context": "",
        "answer": "",
        "revision_count": 0,
        "max_revisions": MAX_REVISIONS,
        "messages": [],
        "final": False,
    }

    result = agent.invoke(initial_state)

    return {
        "question": result.get("question", question),
        "answer": result.get("answer", "No answer generated."),
        "revision_count": result.get("revision_count", 0),
        "context": result.get("context", ""),
        "search_results": result.get("search_results", ""),
    }


# -------------------------------------------------------------------
# CLI entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is RAG and how does it compare to fine-tuning?"
    if not question:
        question = "What is RAG and how does it compare to fine-tuning?"

    print(f"Researching: {question}")
    print(f"Using model: {LLM_MODEL}")
    print("-" * 60)

    result = research(question)

    print(f"\nAnswer ({result['revision_count']} revision(s)):\n")
    print(result["answer"])
