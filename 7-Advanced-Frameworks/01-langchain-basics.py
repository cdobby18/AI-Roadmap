"""Phase 7 - LangChain basics: prompts, LCEL chains, agents, and state.

LangChain 1.3+ is built on LangGraph under the hood. The old "Chain" and
"Memory" classes are gone — replaced by LCEL (| piping) and graph-based agents
with state management.

This file covers:
1. PromptTemplate + ChatPromptTemplate  — parameterized prompts
2. LCEL chains (prompt | model | parser) — the modern replacement for LLMChain
3. Sequential chains with RunnablePassthrough  — pass data between steps
4. Agent with tools (create_agent + @tool decorator)
5. Multi-turn conversation via agent state
"""

from typing import Optional


# ---------------------------------------------------------------------------
# 1. Prompt templates
# ---------------------------------------------------------------------------

def demo_prompt_templates():
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

    template = PromptTemplate.from_template(
        "Explain {concept} in the style of a {audience}."
    )
    prompt = template.invoke({"concept": "RAG", "audience": "five-year-old"})
    print("1. PromptTemplate:")
    print(f"   {prompt.text[:100]}...\n")

    chat = ChatPromptTemplate.from_messages([
        ("system", "You are a {persona} expert. Answer concisely."),
        ("human", "{question}"),
    ])
    msg = chat.invoke({"persona": "RAG", "question": "What is chunking?"})
    print("2. ChatPromptTemplate:")
    for m in msg.messages:
        print(f"   [{m.type}] {m.content[:80]}...")
    print()


# ---------------------------------------------------------------------------
# 2. LCEL chain — the modern replacement for LLMChain
# ---------------------------------------------------------------------------

def demo_lcel_chain():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOllama(model="llama2", temperature=0.0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer in 2-3 sentences."),
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"input": "What is LCEL in LangChain?"})
    print(f"LCEL chain result: {result}\n")


# ---------------------------------------------------------------------------
# 3. Sequential chain — pipe output of one step as input to next
# ---------------------------------------------------------------------------

def demo_sequential():
    from langchain_core.prompts import PromptTemplate
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    llm = ChatOllama(model="llama2", temperature=0.3)
    parser = StrOutputParser()

    summarize = PromptTemplate.from_template(
        "Summarize {topic} in one sentence."
    ) | llm | parser

    extract = PromptTemplate.from_template(
        "Based on this summary, list three key takeaways:\n{summary}"
    ) | llm | parser

    chain = (
        {"summary": summarize}  # first step
        | RunnablePassthrough() # pass summary to next prompt
        | extract
    )

    result = chain.invoke({"topic": "vector databases"})
    print(f"Sequential chain result:\n{result}\n")


# ---------------------------------------------------------------------------
# 4. Agent with tools — create_agent + @tool decorator
# ---------------------------------------------------------------------------

def demo_agent():
    from langchain_core.tools import tool
    from langchain.agents import create_agent
    from langchain_ollama import ChatOllama

    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    @tool
    def word_length(word: str) -> int:
        """Return the number of letters in a word."""
        return len(word)

    llm = ChatOllama(model="llama2", temperature=0.0)
    agent = create_agent(model=llm, tools=[multiply, word_length])

    result = agent.invoke({
        "messages": [("human", "What is 15 multiplied by 7?")],
    })
    print(f"Q: 15 * 7")
    print(f"A: {result['messages'][-1].content}\n")

    result2 = agent.invoke({
        "messages": [("human", "How many letters in 'LangChain'?")],
    })
    print(f"Q: How many letters in 'LangChain'?")
    print(f"A: {result2['messages'][-1].content}\n")


# ---------------------------------------------------------------------------
# 5. Multi-turn conversation — LangGraph checkpointer for state
# ---------------------------------------------------------------------------

def demo_conversation():
    from langchain_core.tools import tool
    from langchain.agents import create_agent
    from langchain_ollama import ChatOllama

    llm = ChatOllama(model="llama2", temperature=0.0)
    agent = create_agent(model=llm, tools=[])
    config = {"configurable": {"thread_id": "demo-session"}}

    print("Conversation:")
    result1 = agent.invoke(
        {"messages": [("human", "Hi! My name is Carl.")]},
        config=config,
    )
    print(f"  Turn 1: {result1['messages'][-1].content}")

    result2 = agent.invoke(
        {"messages": [("human", "What is my name?")]},
        config=config,
    )
    print(f"  Turn 2: {result2['messages'][-1].content}")
    print()


# ---------------------------------------------------------------------------
# Safe runner when Ollama is unavailable
# ---------------------------------------------------------------------------

def try_demo(fn, name: str):
    try:
        fn()
    except Exception as e:
        if "Connection refused" in str(e) or "WinError 10061" in str(e):
            print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve\n")
        else:
            print(f"[ERROR] {name}: {e}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("LangChain Basics — Prompts, LCEL, Agents, State")
    print("=" * 60)

    demo_prompt_templates()
    try_demo(demo_lcel_chain, "LCEL Chain")
    try_demo(demo_sequential, "Sequential Chain")
    try_demo(demo_agent, "Agent")
    try_demo(demo_conversation, "Conversation")
