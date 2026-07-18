# Phase 6 — RAG (Retrieval-Augmented Generation)

## The RAG Pipeline

The core flow: **load → chunk → embed → store → retrieve → augment → generate.**

Every RAG system follows this same sequence. The differences are in how each step is implemented and tuned.

**Why RAG exists:** LLMs have a knowledge cutoff and can hallucinate. RAG provides relevant documents as context, grounding the answer in actual content. This reduces hallucinations, enables question answering over private data, and makes the system auditable.

## Chunking

**What it is:** Splitting documents into smaller pieces that can be retrieved and fed to the LLM as context.

**Strategies (from simplest to most effective):**
- **Fixed-size:** Split every N tokens with optional overlap. Simplest to implement. Can split mid-sentence, breaking semantic coherence.
- **Sentence-aware:** Split at sentence boundaries (`.!?`). More coherent but can produce unevenly sized chunks.
- **Semantic chunking:** Use embedding similarity to detect natural topic boundaries. Produces the most coherent chunks but requires embedding each candidate split point — more compute.

**Why chunking matters more than model choice:** The feedback file says it directly — "Most failures in RAG are chunking failures, not embedding failures." If your chunks don't contain the answer, no amount of retrieval quality or LLM prompt engineering can fix it.

**Best practices:**
- Overlap (10-15% of chunk size) to avoid losing context at boundaries.
- Chunk size depends on use case: 100-200 tokens for Q&A (precision), 500-1000 for summarization (breadth).
- Chunk metadata: tag with source document, section heading, page number, date. Filter on metadata before vector search to halve retrieval noise.

## Embeddings

**What they are:** Dense vector representations of text. Similar texts produce similar vectors (measured by cosine similarity or dot product).

**Sentence-transformers vs BERT:** sentence-transformers are fine-tuned specifically for producing semantically meaningful sentence embeddings (via contrastive learning on NLI/STS datasets). Raw BERT requires mean pooling of token embeddings and produces worse similarity scores. Always prefer sentence-transformers for RAG retrieval.

**Popular models:**
- `all-MiniLM-L6-v2` — 384 dimensions, fast, CPU-friendly. Default choice for prototyping.
- `BAAI/bge-large-en-v1.5` — 1024 dimensions, better quality, more compute. Good for production.
- `intfloat/e5-mistral-7b-instruct` — highest quality, 7B parameters, GPU needed. For retrieval-heavy applications.

**Tradeoff:** Higher dimension = more accurate retrieval (better separation in vector space) + more compute/memory for storage and search.

## Vector Search

**Brute force (FAISS IndexFlatIP):** Compute similarity against every stored vector. O(n) search — fine for up to ~100K vectors. Guarantees exact nearest neighbors.

**Approximate (FAISS IndexIVFFlat, HNSW):** Partition vector space into regions; only search the most promising regions. O(log n) or O(√n) search — needed for millions of vectors. Tradeoff: slight accuracy loss for massive speed gain.

**Hybrid search:** Combine vector similarity with keyword (BM25) overlap. Catches cases where exact keyword matches matter. Use when: retrieval needs to be robust to both semantic similarity and exact term matching (e.g., product search, legal document retrieval).

## Vector Databases Comparison

| System | Best for |
|--------|----------|
| FAISS | Prototypes, small-medium scale, embedded in Python |
| Chroma | Quick prototypes, simple API, built-in embedding |
| Pinecone | Production cloud, fully managed, scales automatically |
| Weaviate / Qdrant | Self-hosted production, hybrid search, multi-tenancy |
| pgvector | Already using PostgreSQL, don't want a separate DB |

**Decision tree:** Start with FAISS + sentence-transformers. If you need persistence across restarts, add Chroma or pgvector. If you need to scale to millions of vectors with zero ops burden, use Pinecone.

## Reranking

**What it is:** After initial retrieval (fast, approximate), a slower but more accurate model re-scores the top candidates.

**Why it's necessary:** Cosine similarity from embeddings is a proxy for relevance, not ground truth. A cross-encoder that jointly processes query + document pair gives much better relevance scores. Typical improvement: top-20 from embedding retrieval → cross-encoder scores → top-5 for LLM context. Boosts relevance metrics by 15-20 points on benchmarks.

**Cross-encoder vs bi-encoder:**
- **Bi-encoder** (embedding model): Encodes query and document independently. Fast (can pre-compute document embeddings). Lower accuracy because query and document don't interact.
- **Cross-encoder** (reranker): Encodes query and document together through the same attention layers. Much more accurate. Cannot pre-compute — must run per query. Adds ~50ms per pair.

**When to rerank:** If you have >10 candidates and need the best 3-5 for the LLM. The LLM's answer quality is limited by the quality of its input context — reranking directly improves that.

## Advanced RAG Patterns

**Query rewriting:** Users ask ambiguous or context-dependent questions ("tell me about that thing from last week"). A small LLM rewrites the query into a standalone, searchable form before retrieval. This is the #1 difference between demo RAG and production RAG.

**Metadata filtering:** Tag chunks with source, date, section, author. Filter before vector search. "Only search documents from 2025" or "only search the 'architecture' section." Halves retrieval noise.

**Self-RAG:** The LLM generates an answer, then retrieves evidence to verify each claim, then revises. More grounded but slower.

**Adaptive RAG:** The system decides how many chunks to retrieve based on the complexity of the query. Simple questions: 1-2 chunks. Complex questions: 5-10 chunks. Saves tokens on easy queries.

**RAG with agentic loops:** Instead of "retrieve once, generate once," the system can retrieve → generate → identify missing info → retrieve again → generate final answer. This is the bridge to LangGraph/agents.

## Evaluation

**RAGAS metrics:**
- **Faithfulness:** Are the claims in the answer supported by the retrieved context? Measures hallucination.
- **Answer relevancy:** Does the answer address the question? Measures whether the LLM stayed on topic.
- **Context precision:** Are the retrieved chunks actually relevant? Measures retrieval quality.
- **Context recall:** Did retrieval capture all the information needed? Measures if chunks are missing.

**Debugging RAG failures:**
1. Retrieve chunks manually — are they relevant? If not: fix chunking or embeddings.
2. If chunks are relevant but answer is wrong: fix prompt or LLM choice.
3. If chunks are missing context: increase chunk size or overlap or number of retrieved chunks.
4. If relevant chunks are ranked low: add reranker.

**Systematic testing:** Create 50-100 test Q&A pairs over your document set. Run them through the pipeline, compute RAGAS metrics, compare across chunking strategies / embedding models / reranker choices. This is the only reliable way to improve a RAG system.

## Interview Must-Knows

- RAG pipeline: load → chunk → embed → store → retrieve → augment → generate.
- Why chunking matters more than model choice.
- Chunking strategies: fixed-size (simplest), sentence-aware (better), semantic (best quality).
- Embedding models: sentence-transformers (MiniLM for speed, BGE for quality).
- FAISS: IndexFlatIP (exact, O(n)) vs IndexIVFFlat (approximate, O(log n)).
- Why reranking is not optional in production: cross-encoder is much more accurate than cosine similarity.
- Query rewriting: the #1 production RAG improvement.
- RAGAS metrics: faithfulness, answer relevancy, context precision.
- Common failure modes and how to debug them.
- Vector DB decision: FAISS for prototype, Chroma/pgvector for persistence, Pinecone for scale.

## Hands-On Files Reference

| File | What It Teaches |
|------|-----------------|
| `01-foundations/01-embeddings-basics.py` | sentence-transformers, creating and comparing embeddings |
| `01-foundations/02-document-chunking.py` | Sentence-aware chunking with overlap |
| `02-retrieval/01-semantic-search.py` | FAISS `IndexFlatIP` + semantic search end-to-end |
| `02-retrieval/02-vector-databases.py` | ChromaDB: persistent vector storage, add/query |
| `02-retrieval/03-hybrid-search.py` | Combining dense vectors + BM25 keyword search |
| `02-retrieval/04-reranking.py` | Cross-encoder reranker for precision boost |
| `02-retrieval/05-faiss-basics.py` | FAISS internals: FlatIP vs IVFFlat, save/load |
| `app/retriever.py` | Production retriever (FAISS singleton pattern) |
| `app/chroma_store.py` | Production retriever (ChromaDB alternative) |
