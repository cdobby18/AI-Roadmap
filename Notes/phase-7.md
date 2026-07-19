# Phase 7 — Advanced Frameworks (LangChain, LangGraph, LangSmith, MCP, Guardrails)

## Overview

Phase 7 moves from calling LLMs directly (Phase 5) and building RAG from scratch (Phase 6) to using **production frameworks** that orchestrate multi-step LLM workflows. These frameworks handle: chaining, memory, tool routing, stateful agents, observability, and safety.

The four pillars:

| Framework | Purpose |
|-----------|---------|
| **LangChain** | High-level abstractions: chains, agents, document loaders, vector stores, prompt templates |
| **LangGraph** | Stateful agentic workflows: graphs with nodes, edges, conditional branching, loops |
| **LangSmith** | Observability: trace every LLM call, evaluate performance, debug failures, manage prompts |
| **MCP (Model Context Protocol)** | Standardized tool interface: expose any resource as a tool an LLM can call |

---

## LangChain

**What it is:** A framework that provides pre-built components for common LLM patterns — chains (sequences of calls), agents (LLM decides which tool to use), document loaders, splitters, vector store integrations, and prompt templates.

**Key concepts:**

- **Chains:** `LLMChain`, `SimpleSequentialChain`, `RouterChain`. Link multiple LLM calls or tool invocations. Each step passes its output as input to the next.
- **Agents:** An LLM chooses which tool(s) to call based on the user's query. Tools are registered with name, description, and JSON schema. The agent observes the tool output and decides next action.
- **Memory:** `ConversationBufferMemory`, `ConversationSummaryMemory`, `VectorStoreRetrieverMemory`. Maintain state across turns. Crucial for chatbots and multi-step tasks.
- **Document loaders:** `TextLoader`, `PyPDFLoader`, `UnstructuredMarkdownLoader` — unified interface for loading any document format.
- **Text splitters:** `RecursiveCharacterTextSplitter`, `SentenceTransformersTokenTextSplitter` — handle chunking with semantic boundary awareness.
- **Vector stores:** `Chroma`, `FAISS`, `PineconeVectorStore` — unified retriever API regardless of backend.
- **Prompt templates:** `PromptTemplate`, `ChatPromptTemplate`, `FewShotPromptTemplate` — parameterized, reusable prompts.

**When to use LangChain:**
- Prototyping RAG pipelines quickly
- When you need pre-built integrations (30+ vector stores, 50+ document loaders)
- Building chains with multiple steps that pass data between each other
- When you want to swap backends (Chroma ↔ Pinecone) without changing application code

**When NOT to use LangChain:**
- Simple single-call LLM use cases (use raw API instead)
- When you need maximum control over every detail (LangChain abstracts things)
- Production at massive scale (overhead of abstractions can add latency)

---

## LangGraph

**What it is:** A library for building **stateful, multi-actor agentic workflows** as graphs. Each node is a function (LLM call, tool, human approval step). Edges define the flow, with conditional routing based on node outputs.

**Key concepts:**

- **Graph:** `StateGraph` — defines nodes and edges. Each invocation runs a traversal from entry node to an end node.
- **State:** A shared dict-like object passed between nodes. Nodes read from and write to state. Supports reducer functions for merging updates (e.g., appending messages).
- **Nodes:** Functions that take state, do work (call LLM, run tool, wait for human input), and return state updates.
- **Edges:** Normal (always go to next node), Conditional (LLM or logic decides which node to go to next), Entry/Exit point.
- **Conditional edges:** The most powerful pattern. The LLM output determines the next step — "should I retrieve more data, or generate the final answer?"

**Agentic loop pattern:**
```
user_input → LLM decides action → execute tool → observe result → 
  → LLM decides: done? → yes → generate final output
                      → no  → pick next tool → loop
```

**When to use LangGraph:**
- Multi-step reasoning where decisions depend on previous steps
- Agentic RAG: retrieve → generate → check if answer is sufficient → retrieve more if not
- Human-in-the-loop workflows: pause, wait for approval, resume
- Parallel execution of independent tasks (e.g., search multiple sources simultaneously)
- Anything that needs a loop, conditional branching, or state persistence

---

## LangSmith

**What it is:** An observability and evaluation platform for LLM applications. Traces every LLM call, tool invocation, and chain step with timing, token usage, and input/output.

**Key features:**

- **Tracing:** Auto-capture every LLM call, retriever query, agent decision. Tree view of complex workflows.
- **Evaluation:** Run test datasets through your system, compare outputs, compute metrics (correctness, latency, cost).
- **Prompt management:** Version prompts, compare variants, deploy to production.
- **Monitoring:** Track latency, error rates, token usage over time. Set alerts.
- **Debugging:** See exactly which chunk was retrieved, what the LLM saw, why it made that decision.

**Why it matters:** Without observability, debugging a RAG pipeline is guessing. With LangSmith, you can replay a specific user query and see every step: "Ah — the retriever returned the wrong chunk because the query wasn't rewritten. Let me fix the rewritter."

---

## MCP (Model Context Protocol)

**What it is:** An open standard (by Anthropic) for connecting LLMs to external tools and data sources. A model context server exposes resources (files, databases, APIs) that the LLM can read and tools the LLM can call.

**Key concepts:**

- **MCP Server:** A lightweight server that exposes capabilities (resources + tools).
- **Resources:** Data the LLM can read (files, DB rows, API responses).
- **Tools:** Functions the LLM can invoke (search, calculate, send email).
- **MCP Client:** The application (LangChain agent, IDE, CLI) that connects to MCP servers.
- **Transport:** Stdio (local processes) or SSE (remote servers).

**Why MCP exists:** Before MCP, every agent framework had its own tool definition format. MCP standardizes how tools are described, discovered, and invoked. Any MCP-compatible agent can use any MCP server's tools without custom integration.

**When to use MCP:**
- Building an agent that needs multiple external tools (web search, DB query, file system)
- Exposing your own APIs as tools for any LLM application to consume
- When you want tool definitions that are framework-agnostic

---

## Guardrails (Output Validation)

**What it is:** Techniques and libraries to ensure LLM outputs are safe, correct, and structured.

**Approaches:**

- **Structured output (API-native):** Use `response_format` (OpenAI) or `grammar` (Ollama) to force valid JSON matching a schema. Zero-cost at inference.
- **Output parsers (LangChain):** `PydanticOutputParser`, `CommaSeparatedListOutputParser` — parse LLM text output into structured types.
- **Validation layer (Guardrails AI / NVIDIA NeMo):** Run output through a validator — check regex, type, allowed values, safety classifiers. Reject and retry if invalid.
- **Content filters:** Block toxic, PII, or off-topic outputs. Can be keyword-based or classifier-based.
- **Jailbreak detection:** Detect prompt injection attempts ("ignore previous instructions") in input.

---

## Integration Patterns

**RAG + LangChain:**
```
loader → splitter → embeddings → vector store → retriever → 
  prompt template → LLM chain → output parser
```
LangChain's `create_retrieval_chain` and `create_history_aware_retriever` wrap this in two function calls.

**Agentic RAG (LangGraph):**
```
graph:
  Node: rewrite_query (LLM) → 
  Node: retrieve (vector store) → 
  Conditional edge: needs more info? → yes → Node: rewrite_query again
                                   → no → Node: generate_answer → END
```

**Multi-LLM routing:**
```
LLM decides: is this a simple query → use local fast model
           : is this complex → use expensive capable model
Route to appropriate provider, measure cost/latency per route.
```

**Cascading fallback:**
```
Try primary model → if fails/timeout → try secondary → if fails → return fallback response
Each step logged and monitored in LangSmith.
```

---

## Interview Must-Knows

- **LangChain vs raw API:** LangChain is for multi-step orchestration, not simple single calls.
- **Agent vs chain:** Chain = predefined sequence. Agent = LLM decides the sequence at runtime.
- **StateGraph vs simple chain:** LangGraph adds state, loops, conditional edges — necessary for any non-linear workflow.
- **MCP vs custom tools:** MCP standardizes tool discovery and invocation. Not needed for 1-2 tools, essential for complex multi-tool agents.
- **Guardrails placement:** Validate input (before LLM) and output (after LLM). Input guards block injection. Output guards enforce structure.
- **Observability first:** Always instrument before optimizing. You can't fix what you can't see.
- **RAG with LangChain:** `create_retrieval_chain(query, retriever)` is a one-liner, but understand what it does internally (retrieve → format → generate).

## Key Tradeoffs

| Decision | Tradeoff |
|----------|----------|
| LangChain vs raw API | Velocity vs control |
| LangGraph vs LangChain agent | Flexibility vs complexity |
| Cloud tracing (LangSmith) vs local (Langfuse) | Managed ease vs data privacy |
| MCP vs built-in tools | Standardization vs simplicity |
| Strict guardrails vs loose | Safety vs user friction |

## Hands-On Files Reference

| File | What It Teaches |
|------|-----------------|
| `01-langchain-basics.py` | Chains, agents, memory, prompt templates |
| `02-langchain-rag.py` | RAG pipeline using LangChain abstractions + Pinecone |
| `03-langgraph-workflows.py` | StateGraph: nodes, edges, conditional routing |
| `04-langgraph-agents.py` | Multi-step agentic patterns (reflection, human-in-loop) |
| `05-langsmith-monitoring.py` | Tracing, evaluation, prompt management |
| `06-guardrails-validation.py` | Output parsers, content filters, jailbreak detection |
| `07-mcp-server-basics.py` | Building and connecting to an MCP server |
| `08-advanced-patterns.py` | Multi-LLM routing, cascading fallback, caching |
