# Research Agent — Architecture Overview

## What It Is

A LangGraph-based multi-agent research system that answers conceptual AI Engineering questions by searching the roadmap notes, synthesizing results, and self-critiquing its answers through a reflection loop.

## Architecture

```
route_question ──► search ──► generate ──► critique
                              ▲                 │
                              │           passed? │
                              └──── no ───────────┘
                                    (max 2 revisions)
                                        │ yes
                                        ▼
                                       END
```

### Nodes

| Node | Function | Key Concept |
|------|----------|-------------|
| `route_question` | Classify question (simple/complex), rewrite for search, pick category | Classification + query rewriting |
| `search` | Execute parallel searches (broad + category-specific) via tools | Tool calling, multi-source retrieval |
| `generate` | Synthesize search results into structured answer with citations | Context engineering, prompt design |
| `critique` | LLM-as-judge: score completeness/accuracy, decide if revision needed | Reflection loop, self-critique |

### Conditional Routing

1. **After `critique`**: If score ≥ 7/10 or max revisions reached → **END**. Otherwise → **search** (revision loop).

## Module Roles

| Module | Responsibility |
|--------|---------------|
| `config.py` | Paths, model settings, revision limits |
| `knowledge_base.py` | Index Notes/ → ChromaDB, chunking, embedding, search |
| `tools.py` | LangChain `@tool` registry (search_knowledge_base, search_by_category) |
| `agent.py` | LangGraph StateGraph, nodes, routing, `research()` entry point |

## Data Sources

All markdown files under `Notes/`:
- `Notes/phases/` — Phase 1-8 concept summaries
- `Notes/reference/` — AI concepts overview, feedback
- `Notes/projects/` — Project documentation + lessons

## How to Run

```bash
# 1. Index the notes (first time only)
python knowledge_base.py
# → Indexed 300+ chunks from 20+ sources

# 2. Run a research query
python agent.py "What is RAG and how does it compare to fine-tuning?"

# 3. Interactive mode
python agent.py "What are the tradeoffs between LangChain and raw API calls?"
```

## Key Phase 7 Concepts Demonstrated

1. **LangGraph StateGraph** — custom state schema, nodes, edges, conditional routing
2. **Reflection loop** — generate → critique → revise, with max revision guard
3. **Tool integration** — LangChain `@tool` decorators, tool registry pattern
4. **LLM-as-judge** — self-evaluation scoring for quality control
5. **Query rewriting** — classification + rewrite for better retrieval
6. **Multi-source search** — broad + category-specific parallel search
7. **LangSmith ready** — set `LANGSMITH_API_KEY` for full tracing

## Future Enhancements

- [ ] Web search tool (Tavily or DuckDuckGo)
- [ ] Streamlit UI for interactive research
- [ ] Citation extraction with source URLs
- [ ] Research report generation (multiple questions → coherent report)
- [ ] MCP server integration for tool discovery
