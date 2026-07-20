# Research Agent — Lessons Learned

## 1. StateGraph State Schema Design

**Lesson:** The state schema (`TypedDict`) defines what data flows between nodes. Every node reads from and writes to this dict. Reducers like `add_messages` control how repeated keys merge (append vs overwrite).

**Key takeaway:** Keep the state schema minimal — only what needs to persist across nodes. Derived data can be recomputed per node.

## 2. Routing by Complexity Is a Force Multiplier

**Lesson:** Classifying questions as "simple" or "complex" before searching lets you optimize resource usage. Simple questions (definitions, facts) need only one search + generate pass. Complex questions (comparisons, design decisions) benefit from the full reflection loop.

**Key takeaway:** Not all queries need agentic overhead. Route smart, not hard.

## 3. Reflection Loops Improve Quality but Need Guardrails

**Lesson:** The biggest improvement comes from the first revision cycle (catching obvious gaps). Diminishing returns set in by revision 2-3. Without a max revision guard, the agent can loop forever — or worse, "revise" a correct answer into an incorrect one.

**Key takeaway:** Always set `max_revisions`. Use LLM-as-judge scoring to decide, but cap the total iterations.

## 4. LLM-as-Judge Is Surprising Reliable for Structural Quality

**Lesson:** Asking the LLM to score its own answer on completeness, citations, and clarity works well. It reliably detects missing source citations, vague claims, and incomplete comparisons. It's less reliable for factual accuracy (the LLM may not know what it doesn't know).

**Key takeaway:** LLM-as-judge excels at structural critique. For factual accuracy, use grounded evaluation (compare against retrieved context).

## 5. Tool Descriptions Are the Agent's API Documentation

**Lesson:** The `@tool` decorator's docstring becomes the tool description the LLM sees. A vague description like "Search for things" leads to poor tool selection. A specific description ("Search the AI Engineering Roadmap knowledge base for concepts, comparisons, tradeoffs...") lets the LLM pick the right tool confidently.

**Key takeaway:** Write tool descriptions as if you're documenting for a developer who's never seen your code.

## 6. Chunking Strategy Depends on Content Type

**Lesson:** The knowledge base has two content types:
- **Phase notes** (dense, structured with headings): Prefer section-aware splitting (by `##` headings) with fallback to sentence boundaries
- **Project notes** (narrative, prose): Standard sentence-aware splitting works well

**Key takeaway:** Use a splitter strategy that matches the document structure. One-size-fits-all chunking leaves quality on the table.

## 7. Parallel Search = Better Coverage

**Lesson:** Running a broad search (all categories) alongside a category-specific search gives better coverage than either alone. The broad search catches unexpected connections; the category search ensures depth.

**Key takeaway:** Default to at least two parallel searches with different scopes. Merge results with deduplication.

## 8. Context Engineering for Multi-Source Answers

**Lesson:** When presenting search results to the LLM, structure them clearly:
```
=== Broad Search Results ===
[Result 1] (score: 0.92) — source name
content...

=== Category: phases ===
[Result 1] (score: 0.88) — source name
content...
```

The LLM produces better answers when it can distinguish between sources and scores.

**Key takeaway:** Format context for the LLM, not for a human reader. Label sections, include scores, keep consistent formatting.

## 9. LangSmith Tracing Is the Debugging Superpower

**Lesson:** With LangSmith enabled, every node execution, LLM call, and tool invocation is captured with timing and input/output. When the agent returns a bad answer, you can replay the trace and see exactly which step failed: "Ah — the question was classified wrong, so it searched the wrong category."

**Key takeaway:** Instrument early. Add `LANGSMITH_API_KEY` and `LANGCHAIN_TRACING_V2=true` to your env before running. A trace is worth a thousand print statements.

## 10. Agentic RAG vs Simple RAG: The Tradeoff

| Aspect | Simple RAG | Agentic RAG (this project) |
|--------|-----------|---------------------------|
| Latency | ~5-10s | ~20-60s (multiple LLM calls) |
| Quality | Good for simple questions | Better for complex, comparative questions |
| Cost | 1-2 LLM calls | 4-8 LLM calls (routing + search + generate + critique × revisions) |
| Debugging | Trivial | Requires tracing (LangSmith) |
| Use case | Chatbots, Q&A | Research, analysis, decision support |

**Key takeaway:** Use agentic RAG when the question is worth the overhead. For a chat interface, simple RAG is often sufficient. This project demonstrates the agentic pattern so you can decide when to apply it.
