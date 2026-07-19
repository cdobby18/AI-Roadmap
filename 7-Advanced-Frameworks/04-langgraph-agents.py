"""Phase 7 - LangGraph advanced agent patterns.

Building on StateGraph basics, this file covers patterns that make
agents reliable in production.

Patterns covered:
1. Reflection loop — generate -> critique -> revise -> output
2. Human-in-the-loop — pause for approval before executing
3. Parallel tool execution — search multiple sources simultaneously
"""

from typing import TypedDict, Annotated, List


# ---------------------------------------------------------------------------
# 1. Reflection loop: generate -> critique -> revise -> output
# ---------------------------------------------------------------------------

def demo_reflection_loop():
    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

    class ReflectionState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]
        draft: str
        critique: str
        revision_count: int

    def generate_draft(state: ReflectionState):
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama2", temperature=0.5)
        question = state["messages"][-1].content
        prompt = f"Write a clear, concise answer to: {question}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"draft": response.content, "messages": [response], "revision_count": 0}

    def critique_draft(state: ReflectionState):
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama2", temperature=0.3)
        prompt = f"Critique this answer. What's missing or inaccurate?\n\n{state['draft']}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"critique": response.content}

    def revise_draft(state: ReflectionState):
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama2", temperature=0.3)
        prompt = f"Original answer:\n{state['draft']}\n\nCritique:\n{state['critique']}\n\nRevise the answer based on the critique."
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"draft": response.content, "messages": [response], "revision_count": state["revision_count"] + 1}

    def should_continue_reflecting(state: ReflectionState):
        if state["revision_count"] >= 2:
            return "end"
        return "critique"

    graph = StateGraph(ReflectionState)
    graph.add_node("generate", generate_draft)
    graph.add_node("critique", critique_draft)
    graph.add_node("revise", revise_draft)
    graph.set_entry_point("generate")
    graph.add_edge("generate", "critique")
    graph.add_conditional_edges("critique", should_continue_reflecting, {
        "critique": "revise",
        "end": "__end__",
    })
    graph.add_edge("revise", "critique")
    app = graph.compile()

    result = app.invoke({"messages": [HumanMessage(content="What is the difference between Haki and Devil Fruits?")]})
    print(f"1. Reflection loop ({result['revision_count']} revisions):")
    print(f"   {result['draft'][:200]}...\n")


# ---------------------------------------------------------------------------
# 2. Human-in-the-loop — pause for approval before executing tools
# ---------------------------------------------------------------------------

def demo_human_in_loop():
    import sys
    if not sys.stdin.isatty():
        print("\n   [SKIP] Human-in-loop requires interactive terminal. Run directly with: python 04-langgraph-agents.py")
        return

    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

    class HumanLoopState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]
        proposed_tool: str
        approved: bool

    def propose_action(state: HumanLoopState):
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama2", temperature=0.0)
        question = state["messages"][-1].content
        prompt = f"Propose which tool to use for: {question}. Options: web_search, database_query, none."
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"proposed_tool": response.content.strip().lower(), "approved": False}

    def human_approval(state: HumanLoopState):
        print(f"\n   [HUMAN] Proposed action: {state['proposed_tool']}")
        print(f"   [HUMAN] Approve? (y/n): ", end="")
        choice = input().strip().lower()
        return {"approved": choice == "y"}

    def execute_action(state: HumanLoopState):
        from langchain_ollama import ChatOllama
        if not state["approved"]:
            return {"messages": [HumanMessage(content="Action rejected by user.")]}
        llm = ChatOllama(model="llama2", temperature=0.0)
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def route_after_human(state: HumanLoopState):
        return "execute" if state["approved"] else "__end__"

    graph = StateGraph(HumanLoopState)
    graph.add_node("propose", propose_action)
    graph.add_node("human", human_approval)
    graph.add_node("execute", execute_action)
    graph.set_entry_point("propose")
    graph.add_edge("propose", "human")
    graph.add_conditional_edges("human", route_after_human, {
        "execute": "execute",
        "__end__": "__end__",
    })
    graph.set_finish_point("execute")
    app = graph.compile()

    result = app.invoke({
        "messages": [HumanMessage(content="Search for information about the One Piece treasure.")],
    })
    print(f"\n2. Human-in-loop result: {result['messages'][-1].content}\n")


# ---------------------------------------------------------------------------
# 3. Parallel execution — search multiple sources simultaneously
# ---------------------------------------------------------------------------

def demo_parallel_execution():
    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

    class ParallelState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]
        results: dict
        final_answer: str

    def search_web(state: ParallelState):
        topic = state["messages"][-1].content
        return {"results": {"web": f"Web results about {topic}: served via search API"}}

    def search_db(state: ParallelState):
        topic = state["messages"][-1].content
        return {"results": {"db": f"DB results about {topic}: from local knowledge base"}}

    def search_rag(state: ParallelState):
        topic = state["messages"][-1].content
        from langchain_ollama import OllamaEmbeddings
        from langchain_core.vectorstores import InMemoryVectorStore
        from langchain_core.documents import Document

        docs = [Document(page_content="One Piece is the legendary treasure left by Gol D. Roger.")]
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vs = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
        results = vs.similarity_search(topic, k=1)
        return {"results": {"rag": results[0].page_content if results else "No results"}}

    def synthesize(state: ParallelState):
        from langchain_ollama import ChatOllama
        all_results = "\n".join(f"- {k}: {v}" for k, v in state["results"].items())
        llm = ChatOllama(model="llama2", temperature=0.0)
        prompt = f"Synthesize these search results into one answer:\n{all_results}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"messages": [response], "final_answer": response.content}

    graph = StateGraph(ParallelState)
    graph.add_node("web", search_web)
    graph.add_node("db", search_db)
    graph.add_node("rag", search_rag)
    graph.add_node("synthesize", synthesize)

    graph.set_entry_point("web")
    graph.add_edge("web", "db")
    graph.add_edge("db", "rag")
    graph.add_edge("rag", "synthesize")
    graph.set_finish_point("synthesize")
    app = graph.compile()

    result = app.invoke({
        "messages": [HumanMessage(content="What is One Piece?")],
    })
    print(f"3. Parallel (sequential simulated) answer:\n   {result['final_answer'][:200]}...\n")


# ---------------------------------------------------------------------------
# Safe runner
# ---------------------------------------------------------------------------

def try_demo(fn, name: str):
    try:
        fn()
    except (ConnectionError, ConnectionRefusedError):
        print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve\n")
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "WinError 10061" in msg:
            print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve\n")
        else:
            import traceback
            print(f"[ERROR] {name}: {msg}")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    print("=" * 60)
    print("LangGraph Advanced — Reflection, Human-in-Loop, Parallel")
    print("=" * 60)
    try_demo(demo_reflection_loop, "Reflection Loop")
    print("   (Human-in-loop requires interactive input — run directly)")
    try_demo(demo_parallel_execution, "Parallel Execution")
