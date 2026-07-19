"""Phase 7 - Advanced patterns: multi-LLM routing, cascading fallback, caching.

Production LLM apps need resilience — when one model is down or too slow,
the system should degrade gracefully. These patterns make pipelines fault-tolerant
and cost-efficient.

This file covers:
1. Multi-LLM routing — classify complexity, route to the right model
2. Cascading fallback — try primary, fall back through a chain of models
3. Embedding cache — avoid redundant embedding computations
"""

import hashlib


# ---------------------------------------------------------------------------
# 1. Multi-LLM routing — route by task complexity
# ---------------------------------------------------------------------------

def demo_multi_llm_routing():
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    classifier_prompt = ChatPromptTemplate.from_messages([
        ("system", "Classify the question as 'simple' or 'complex'. "
         "Simple: factual, one-hop. Complex: multi-step, analytical.\n"
         "Return only the word: simple or complex."),
        ("human", "{question}"),
    ])
    llm = ChatOllama(model="llama2", temperature=0.0)
    classifier = classifier_prompt | llm | StrOutputParser()

    simple_llm = ChatOllama(model="llama2", temperature=0.0)
    complex_llm = ChatOllama(model="llama2", temperature=0.3)

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer concisely."),
        ("human", "{question}"),
    ])
    simple_chain = answer_prompt | simple_llm | StrOutputParser()
    complex_chain = answer_prompt | complex_llm | StrOutputParser()

    def route(question: str) -> str:
        label = classifier.invoke({"question": question}).strip().lower()
        chain = simple_chain if "simple" in label else complex_chain
        return chain.invoke({"question": question})

    print("1. Multi-LLM routing:")
    questions = [
        ("simple", "What is Luffy's Devil Fruit called?"),
        ("complex", "Compare Zoro's and Sanji's fighting styles and explain their respective roles in the crew."),
    ]
    for expected, q in questions:
        answer = route(q)
        print(f"   [{expected}] Q: {q[:50]}...")
        print(f"   A: {answer[:120]}...")
        print()
    print()


# ---------------------------------------------------------------------------
# 2. Cascading fallback — try primary, then secondary, then tertiary
# ---------------------------------------------------------------------------

def demo_cascading_fallback():
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer concisely."),
        ("human", "{input}"),
    ])

    models = [
        ("llama2-high-perf", ChatOllama(model="llama2", temperature=0.0)),
        ("llama2-backup", ChatOllama(model="llama2", temperature=0.0)),
    ]

    def ask_with_fallback(question: str) -> tuple[str, str]:
        last_error = None
        for name, llm in models:
            try:
                chain = prompt | llm | StrOutputParser()
                answer = chain.invoke({"input": question})
                return name, answer
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(f"All models failed. Last error: {last_error}")

    print("2. Cascading fallback:")
    name, answer = ask_with_fallback("What is the One Piece treasure?")
    print(f"   Served by: {name}")
    print(f"   Answer: {answer[:120]}...")
    print()

    # Simulate first model failure
    print("   Simulating primary failure...")
    models.insert(0, ("broken-model", "not-a-model"))
    try:
        name, answer = ask_with_fallback("Who is the Pirate King?")
        print(f"   Served by: {name}")
        print(f"   Answer: {answer[:120]}...")
    except Exception as e:
        print(f"   [FALLBACK FAILED] {e}")
    print()


# ---------------------------------------------------------------------------
# 3. Embedding cache — avoid recomputing embeddings for seen texts
# ---------------------------------------------------------------------------

def demo_embedding_cache():
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_core.documents import Document

    class DummyEmbeddings:
        """Stub embeddings that work without Ollama — illustrates caching logic."""

        def __init__(self):
            self._cache: dict[str, list[float]] = {}

        def embed_query(self, text: str) -> list[float]:
            key = hashlib.sha256(text.encode()).hexdigest()
            if key in self._cache:
                print(f"   [CACHE HIT] '{text[:40]}...'")
                return self._cache[key]
            vec = [float(ord(c)) for c in text[:64]] + [0.0] * (64 - min(64, len(text)))
            self._cache[key] = vec
            print(f"   [CACHE MISS] '{text[:40]}...'")
            return vec

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [self.embed_query(t) for t in texts]

    print("3. Embedding cache:")
    texts = [
        "Luffy ate the Gomu Gomu no Mi",
        "Zoro is a master swordsman",
        "Luffy ate the Gomu Gomu no Mi",
        "Nami is the best navigator",
        "Zoro is a master swordsman",
    ]

    embeddings = DummyEmbeddings()
    vectors = [embeddings.embed_query(t) for t in texts]

    print(f"\n   Total queries: {len(texts)}")
    print(f"   Cache entries: {len(embeddings._cache)}")
    print(f"   Cache hits: {len(texts) - len(embeddings._cache)}")

    docs = [Document(page_content=t) for t in ["Luffy ate the Gomu Gomu no Mi", "Zoro is a master swordsman"]]
    vs = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
    results = vs.similarity_search("Luffy fruit", k=1)
    print(f"   Query 'Luffy fruit' found: {results[0].page_content}")

    print("\n   To use with real Ollama embeddings, replace DummyEmbeddings with:")
    print("     from langchain_ollama import OllamaEmbeddings")
    print("     embeddings = CachedEmbeddings(OllamaEmbeddings(model='nomic-embed-text'))")
    print()


# ---------------------------------------------------------------------------
# Safe runner
# ---------------------------------------------------------------------------

def try_demo(fn, name: str):
    try:
        fn()
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
    print("Advanced Patterns — Routing, Fallback, Embedding Cache")
    print("=" * 60)
    try_demo(demo_multi_llm_routing, "Multi-LLM Routing")
    try_demo(demo_cascading_fallback, "Cascading Fallback")
    try_demo(demo_embedding_cache, "Embedding Cache")
