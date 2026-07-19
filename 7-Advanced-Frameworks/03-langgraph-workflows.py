"""Phase 7 - LangGraph workflows: StateGraph, nodes, edges, conditional routing.

LangGraph turns LLM workflows into directed graphs. Each node is a step
(retrieve, generate, critique) and edges define the flow — including
conditional branches where the LLM decides what to do next.

This file covers:
1. Simple linear graph (retrieve -> generate)
2. Conditional routing (check if context is sufficient, route accordingly)
3. State management across steps
"""

from typing import TypedDict, Annotated, List
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Simple linear graph: retrieve -> generate
# ---------------------------------------------------------------------------

def demo_linear_graph():
    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
    from langchain_core.documents import Document
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_ollama import OllamaEmbeddings, ChatOllama

    # --- state schema ---
    class RagState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]
        context: str

    # --- setup ---
    docs = [
        Document(page_content="Luffy ate the Gomu Gomu no Mi, a Paramecia-type Devil Fruit.")
    ]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    # --- node functions ---
    def retrieve_node(state: RagState):
        question = state["messages"][-1].content
        results = retriever.invoke(question)
        context = "\n\n".join(d.page_content for d in results)
        return {"context": context}

    def generate_node(state: RagState):
        llm = ChatOllama(model="llama2", temperature=0.0)
        prompt = f"Answer using this context:\n{state['context']}\n\nQuestion: {state['messages'][-1].content}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"messages": [response]}

    # --- build graph ---
    graph = StateGraph(RagState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.set_finish_point("generate")
    app = graph.compile()

    result = app.invoke({"messages": [HumanMessage(content="What Devil Fruit did Luffy eat?")]})
    print(f"1. Linear graph answer: {result['messages'][-1].content}\n")


# ---------------------------------------------------------------------------
# 2. Conditional routing — check context before generating
# ---------------------------------------------------------------------------

def demo_conditional_graph():
    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
    from langchain_core.documents import Document
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_ollama import OllamaEmbeddings, ChatOllama

    class RagState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]
        context: str
        needs_retry: bool

    docs = [
        Document(page_content="The Grand Line is a sea between the Red Line and the Calm Belt.")
    ]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    def retrieve_node(state: RagState):
        question = state["messages"][-1].content
        results = retriever.invoke(question)
        context = "\n\n".join(d.page_content for d in results)
        return {"context": context, "needs_retry": False}

    def check_node(state: RagState):
        llm = ChatOllama(model="llama2", temperature=0.0)
        prompt = f"Does the context below answer: {state['messages'][-1].content}?\nContext: {state['context']}\nAnswer only YES or NO."
        response = llm.invoke([SystemMessage(content=prompt)])
        answer = response.content.strip().upper()
        return {"needs_retry": "NO" in answer}

    def rewrite_node(state: RagState):
        llm = ChatOllama(model="llama2", temperature=0.3)
        original = state["messages"][-1].content
        prompt = f"Rewrite this query to be more searchable: {original}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"messages": [HumanMessage(content=response.content)], "needs_retry": False}

    def generate_node(state: RagState):
        llm = ChatOllama(model="llama2", temperature=0.0)
        prompt = f"Answer using this context:\n{state['context']}\n\nQuestion: {state['messages'][-1].content}"
        response = llm.invoke([SystemMessage(content=prompt)])
        return {"messages": [response]}

    def route_after_check(state: RagState):
        return "rewrite" if state["needs_retry"] else "generate"

    # --- build graph ---
    graph = StateGraph(RagState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("check", check_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "check")
    graph.add_conditional_edges("check", route_after_check, {
        "rewrite": "rewrite",
        "generate": "generate",
    })
    graph.add_edge("rewrite", "generate")
    graph.set_finish_point("generate")
    app = graph.compile()

    result = app.invoke({"messages": [HumanMessage(content="Tell me about the Grand Line")]})
    print(f"2. Conditional graph answer: {result['messages'][-1].content}\n")


# ---------------------------------------------------------------------------
# 3. Agent with tool loop — LangGraph version
# ---------------------------------------------------------------------------

def demo_agent_loop():
    from langgraph.graph import StateGraph, add_messages
    from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
    from langchain_core.tools import tool
    from langchain_ollama import ChatOllama

    @tool
    def search_crew(member: str) -> str:
        """Get information about a Straw Hat crew member."""
        crew = {
            "luffy": "Monkey D. Luffy, captain, Gomu Gomu no Mi, wants to be Pirate King",
            "zoro": "Roronoa Zoro, swordsman, three swords, wants to be world's greatest",
            "nami": "Nami, navigator, can sense weather, wants to map the world",
            "sanji": "Sanji, chef, Black Leg style, wants to find the All Blue",
            "robin": "Nico Robin, archaeologist, Hana Hana no Mi, seeks true history",
        }
        return crew.get(member.lower(), f"No info on {member}")

    class AgentState(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]

    def call_model(state: AgentState):
        llm = ChatOllama(model="llama2", temperature=0.0)
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def execute_tool(state: AgentState):
        last = state["messages"][-1]
        if not hasattr(last, "tool_calls") or not last.tool_calls:
            return {"messages": []}

        tool_map = {"search_crew": search_crew}
        results = []
        for tc in last.tool_calls:
            result = tool_map[tc["name"]].invoke(tc["args"])
            results.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        return {"messages": results}

    def should_continue(state: AgentState):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "continue"
        return "end"

    graph = StateGraph(AgentState)
    graph.add_node("model", call_model)
    graph.add_node("tools", execute_tool)
    graph.set_entry_point("model")
    graph.add_conditional_edges("model", should_continue, {
        "continue": "tools",
        "end": "__end__",
    })
    graph.add_edge("tools", "model")
    app = graph.compile()

    result = app.invoke({
        "messages": [HumanMessage(content="Tell me about Zoro and Robin")],
    })
    print(f"3. Agent loop answer: {result['messages'][-1].content}\n")


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
    print("LangGraph Workflows — StateGraph, Nodes, Conditional Edges")
    print("=" * 60)
    try_demo(demo_linear_graph, "Linear Graph")
    try_demo(demo_conditional_graph, "Conditional Graph")
    try_demo(demo_agent_loop, "Agent Loop")
