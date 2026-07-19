"""Phase 7 - LangSmith: tracing, evaluation, and observability.

LangSmith gives you visibility into every LLM call, retriever query, and
agent decision. Without observability, debugging a RAG pipeline is guessing —
you can't see which chunk was retrieved, what the LLM actually received,
or why it made a particular decision.

This file covers:
1. Setting up LangSmith tracing (environment variables)
2. Tracing a chain automatically
3. Tracing with project and run name
4. Basic evaluation concepts
"""

import os


# ---------------------------------------------------------------------------
# 1. LangSmith setup
# ---------------------------------------------------------------------------

def check_setup():
    """Check if LangSmith is configured. Tracing requires an API key."""
    api_key = os.environ.get("LANGSMITH_API_KEY", "")
    project = os.environ.get("LANGSMITH_PROJECT", "")
    endpoint = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

    print("1. LangSmith Configuration:")
    print(f"   LANGSMITH_API_KEY: {'[OK]' if api_key else '[MISSING]'}")
    print(f"   LANGSMITH_PROJECT: '{project}'" if project else "   LANGSMITH_PROJECT: 'default'")
    print(f"   LANGSMITH_ENDPOINT: {endpoint}")

    if not api_key:
        print("\n   -> To enable tracing, set:")
        print("     export LANGSMITH_API_KEY='your-api-key'")
        print("     export LANGSMITH_PROJECT='my-rag-app'")
        print("   Get a key at: https://smith.langchain.com")
    return bool(api_key)


# ---------------------------------------------------------------------------
# 2. Auto-tracing a chain
# ---------------------------------------------------------------------------

def demo_tracing(has_api_key: bool):
    """Run a chain with LangSmith tracing."""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_ollama import OllamaEmbeddings
    from langchain_core.documents import Document

    if not has_api_key:
        print("\n2. Tracing (configured, but no API key — runs without tracing):")

    docs = [
        Document(page_content="RAG combines retrieval with generation for grounded answers."),
        Document(page_content="LangSmith traces every step of the RAG pipeline."),
    ]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using the retrieved context."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])
    llm = ChatOllama(model="llama2", temperature=0.0)
    parser = StrOutputParser()

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | parser
    )

    # LangSmith auto-traces if LANGSMITH_API_KEY is set
    result = chain.invoke("What is RAG and how does LangSmith help?")
    print(f"   Traced RAG answer: {result[:120]}...")

    if has_api_key:
        print("   -> View trace at: https://smith.langchain.com")
    print()


# ---------------------------------------------------------------------------
# 3. Run with named project
# ---------------------------------------------------------------------------

def demo_named_run():
    """Run a chain under a specific project name using run_name."""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableConfig

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer concisely."),
        ("human", "{input}"),
    ])
    llm = ChatOllama(model="llama2", temperature=0.0)
    chain = prompt | llm | StrOutputParser()

    config = RunnableConfig(
        run_name="phase-7-demo-answer",
        tags=["demo", "phase-7"],
        metadata={"phase": "7", "topic": "langsmith"},
    )
    result = chain.invoke({"input": "What is the Grand Line?"}, config=config)
    print(f"3. Named run: {result[:120]}...")
    print("   -> Tags and metadata attached to this trace in LangSmith\n")


# ---------------------------------------------------------------------------
# 4. Evaluation concepts
# ---------------------------------------------------------------------------

def demo_evaluation_concepts():
    """Show how evaluation datasets work in LangSmith (conceptual)."""
    print("4. LangSmith Evaluation (conceptual):")

    print("""
   LangSmith lets you create test datasets and run evaluations:

   from langsmith import Client
   client = Client()

   # Create a dataset
   dataset = client.create_dataset("rag-test-set")
   client.create_examples(
       inputs=[{"question": "What is RAG?"}],
       outputs=[{"answer": "RAG is retrieval-augmented generation."}],
       dataset_id=dataset.id,
   )

   # Run evaluation
   from langsmith.evaluation import evaluate
   results = evaluate(
       lambda inputs: chain.invoke(inputs["question"]),
       data="rag-test-set",
       evaluators=[...],
   )
   """)

    print("   Key evaluators you can use:")
    print("   - qa_correctness — exact match / semantic similarity")
    print("   - criteria — LLM-as-judge (helpfulness, conciseness)")
    print("   - labeled_criteria — compare against ground truth")
    print("   - pairwise — A/B compare two system versions\n")


# ---------------------------------------------------------------------------
# Safe runner
# ---------------------------------------------------------------------------

def try_demo(fn, name: str, *args):
    try:
        fn(*args)
    except (ConnectionError, ConnectionRefusedError) as e:
        print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve")
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "WinError 10061" in msg:
            print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve")
        else:
            import traceback
            print(f"[ERROR] {name}: {msg}")
            traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("LangSmith — Observability, Tracing, Evaluation")
    print("=" * 60)

    has_key = check_setup()
    print()

    try_demo(demo_tracing, "Tracing Demo", has_key)
    try_demo(demo_named_run, "Named Run")
    demo_evaluation_concepts()
