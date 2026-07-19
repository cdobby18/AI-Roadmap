"""Phase 7 - RAG with LangChain: load, split, embed, retrieve, generate.

LangChain provides abstractions over the full RAG pipeline so you can swap
backends (Chroma ↔ InMemory ↔ Pinecone) without changing application code.

This file covers:
1. Text splitting with RecursiveCharacterTextSplitter
2. Embedding + vector store with InMemoryVectorStore
3. Retriever + LCEL RAG chain (retrieve -> prompt -> generate)
4. Conversational RAG with history-aware retrieval
"""

from pathlib import Path
from typing import List


# ---------------------------------------------------------------------------
# 1. Load and split documents
# ---------------------------------------------------------------------------

def load_and_split(data_dir: str = "data/sample_docs"):
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    docs: List[Document] = []
    for path in sorted(Path(data_dir).glob("*.txt")):
        content = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=content, metadata={"source": path.name}))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40,
        separators=["\n\n", "\n", ".", "!", "?", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"1. Loaded {len(docs)} documents -> {len(chunks)} chunks")
    return chunks


# ---------------------------------------------------------------------------
# 2. Embed and store in vector DB
# ---------------------------------------------------------------------------

def build_vector_store(chunks):
    from langchain_ollama import OllamaEmbeddings
    from langchain_core.vectorstores import InMemoryVectorStore

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
    print(f"2. Indexed {len(chunks)} chunks in InMemoryVectorStore")
    return vector_store


# ---------------------------------------------------------------------------
# 3. Basic RAG chain — retrieve -> prompt -> generate
# ---------------------------------------------------------------------------

def demo_basic_rag(vector_store):
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model="llama2", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the retrieved context to answer the question. "
                    "If you don't know, say so."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    question = "What is RAG and why does it matter?"
    answer = chain.invoke(question)
    print(f"\n3. Basic RAG:")
    print(f"   Q: {question}")
    print(f"   A: {answer}")


# ---------------------------------------------------------------------------
# 4. Conversational RAG — with chat history
# ---------------------------------------------------------------------------

def demo_conversational_rag(vector_store):
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.messages import HumanMessage, AIMessage

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model="llama2", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the retrieved context to answer."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough(), "history": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    history = [
        HumanMessage(content="What is chunking?"),
        AIMessage(content="Chunking splits documents into smaller pieces for retrieval."),
    ]

    question = "How does chunk size affect retrieval quality?"
    answer = chain.invoke({"question": question, "history": history})
    print(f"\n4. Conversational RAG:")
    print(f"   History: Q: What is chunking? A: ...")
    print(f"   Q: {question}")
    print(f"   A: {answer}")


# ---------------------------------------------------------------------------
# 5. History-aware retrieval — rewrite query using chat history
# ---------------------------------------------------------------------------

def demo_history_aware_retrieval():
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_ollama import ChatOllama, OllamaEmbeddings
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_core.runnables import RunnablePassthrough
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    from langchain_core.messages import HumanMessage, AIMessage

    # --- setup ---
    docs = [
        "Vector databases store embeddings for fast similarity search.",
        "FAISS is an in-memory vector index for small to medium datasets.",
        "ChromaDB is a persistent vector database with metadata filtering.",
        "Pinecone is a fully managed cloud vector database for production.",
    ]
    chunks = [Document(page_content=t) for t in docs]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    llm = ChatOllama(model="llama2", temperature=0.0)

    # --- query rewriter using history ---
    rewriter_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given the chat history and the latest question, "
                    "rewrite it as a standalone search query."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    rewriter = rewriter_prompt | llm | StrOutputParser()

    # --- answer chain ---
    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using the retrieved context."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    answer_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | answer_prompt
        | llm
        | StrOutputParser()
    )

    # --- full chain: rewrite -> retrieve -> answer ---
    history = [
        HumanMessage(content="What is FAISS?"),
        AIMessage(content="FAISS is an in-memory vector index."),
    ]
    question = "How does it compare to ChromaDB?"

    rewritten = rewriter.invoke({"question": question, "history": history})
    answer = answer_chain.invoke(rewritten)

    print(f"\n5. History-aware retrieval:")
    print(f"   Original: {question}")
    print(f"   Rewritten: {rewritten}")
    print(f"   A: {answer}")


# ---------------------------------------------------------------------------
# Safe runner
# ---------------------------------------------------------------------------

def try_demo(fn, name: str, *args):
    try:
        fn(*args)
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "WinError 10061" in msg:
            print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve")
        else:
            print(f"[ERROR] {name}: {msg}")


if __name__ == "__main__":
    print("=" * 60)
    print("LangChain RAG — Load, Split, Embed, Retrieve, Generate")
    print("=" * 60)

    chunks = load_and_split()
    vector_store = try_demo(build_vector_store, "Vector Store", chunks)

    if vector_store is not None:
        try_demo(demo_basic_rag, "Basic RAG", vector_store)
        try_demo(demo_conversational_rag, "Conversational RAG", vector_store)

    try_demo(demo_history_aware_retrieval, "History-aware RAG")
