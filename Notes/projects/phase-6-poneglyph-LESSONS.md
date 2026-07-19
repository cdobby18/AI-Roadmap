# Poneglyph Reader — Lessons & Concepts

> The conceptual explanations behind every module in the Poneglyph Reader.

---

## 1. Web Scraping (`scraper.py`)

### Why scrape instead of using a dataset?

Real RAG systems ingest **live data** from APIs or websites — docs, wikis, knowledge bases. You can't control the format. You have to handle:
- Inconsistent HTML structure
- Missing pages (404s)
- Rate limits
- Encoding issues

### How the scraper works

1. **Fetch** — HTTP GET the wiki page with a User-Agent header
2. **Parse** — BeautifulSoup extracts text from `div.mw-parser-output`
3. **Section** — Preserves heading hierarchy (`h2`, `h3` become `##` sections)
4. **Classify** — Heuristic tags (character, devil_fruit, location) for metadata filtering
5. **Cache** — Raw HTML saved to disk so you don't re-scrape during dev

### Key tradeoffs

| Approach | Pro | Con |
|----------|-----|-----|
| requests + BeautifulSoup | Simple, no external deps | Fragile to HTML changes |
| Fandom API | Structured JSON | Less educational (hides parsing) |
| Selenium/Playwright | Handles JS-rendered content | Heavy, slow |

### Rate limiting

```python
time.sleep(SCRAPER_DELAY)  # 1 second between requests
```

Without this, you'll get IP-banned. Most wikis allow ~1 req/sec.

---

## 2. Text Chunking (`ingestion.py`)

### Why chunk?

LLMs have **context windows** (typically 4K-8K tokens). A single wiki page can be 10K+ tokens. Chunking:
- Makes every piece small enough to fit in context
- Lets you retrieve only the relevant pieces
- Keeps vector search fast (comparing short vectors vs. long ones)

### Sentence-aware splitting

```
Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5.
                                                          
[Chunk 1: Sentence 1-3]                                  
[Chunk 2: Sentence 3-5]  ← overlap preserves transition
```

**Why not word-level?** Cutting mid-sentence loses meaning. Sentence boundaries (`.`, `!`, `?`) are natural semantic units.

### Overlap

Without overlap, the connection between chunks is lost:

```
Chunk 1: "Luffy ate the Gomu Gomu no Mi. It gives him rubber"
Chunk 2: "properties. He can stretch his body."                 ← "properties" has no context
```

With overlap:
```
Chunk 1: "Luffy ate the Gomu Gomu no Mi. It gives him rubber"
Chunk 2: "rubber properties. He can stretch his body."          ← "rubber" carries over
```

### Chunk size tradeoff

| Chunk size | Pros | Cons |
|-----------|------|------|
| Small (50-100 words) | Precise retrieval, more targeted | Loses broader context |
| Medium (150-250 words) | Good balance | Some irrelevant details |
| Large (300-500 words) | Rich context | Diluted relevance, slower search |

The config uses **200 words** with **40 overlap** — a balanced default.

---

## 3. Embedding Models (`ingestion.py`)

### What is an embedding?

An embedding is a **dense vector** (list of floats) that captures the semantic meaning of text. Similar texts have similar vectors.

```
"Luffy is a pirate"  →  [0.23, -0.45, 0.78, ..., 0.12]  (384 numbers)
"Captain Luffy"      →  [0.25, -0.42, 0.80, ..., 0.10]  (close by)
"Ramen is delicious" →  [-0.15, 0.33, -0.21, ..., 0.05]  (far away)
```

### Bi-encoder vs Cross-encoder

| | Bi-encoder (sentence-transformers) | Cross-encoder |
|---|---|---|
| How | Encodes query and doc separately | Processes (query, doc) together |
| Speed | Fast — pre-compute doc vectors | Slow — must process each pair |
| Accuracy | Good for retrieval | Excellent for reranking |
| Use case | First-stage retrieval | Second-stage reranking |

The **bi-encoder** (`all-MiniLM-L6-v2`) is used for vector search — it embeds all documents once at index time, then embeds only the query at search time.

The **cross-encoder** (`ms-marco-MiniLM-L-6-v2`) is used for reranking — it takes the top-K from the bi-encoder and scores each (query, doc) pair jointly for better precision.

### Why not use a cross-encoder for everything?

It doesn't scale. A cross-encoder processes O(N) pairs per query. With 10,000 documents, that's 10,000 forward passes per question. The bi-encoder does 1 forward pass per query + a fast nearest-neighbor search.

---

## 4. Vector Search (`rag.py`)

### How ChromaDB works

ChromaDB is a **vector database** — it stores (vector, text, metadata) triples and retrieves them by similarity.

1. **Indexing**: Documents are embedded and stored with their vectors
2. **Querying**: Question is embedded, then ChromaDB finds nearest neighbors
3. **Distance metric**: Cosine similarity (1 - cosine distance)

```
Collection "poneglyph_reader"
┌────────────────────────────────────────┐
│ ID        │ Vector (384d)  │ Text      │
│───────────┼───────────────┼───────────│
│ luffy_0   │ [0.23, -0.45] │ "Luffy..."│
│ zoro_1    │ [-0.12, 0.78] │ "Zoro..." │
│ ...       │ ...           │ ...       │
└────────────────────────────────────────┘
```

ChromaDB uses **HNSW** (Hierarchical Navigable Small World) graphs for approximate nearest neighbor search — the same algorithm powering Pinecone and Qdrant.

### Metadata filtering

You can filter by category before the search:

```python
collection.query(
    query_embeddings=query_vec,
    where={"categories": {"$contains": "character"}},
)
```

This narrows the search to only character pages. Important for production — users often want to search within a domain.

---

## 5. Reranking (`rag.py`)

### The two-stage pattern

```
Query: "What is Luffy's Devil Fruit?"

Stage 1 (Bi-encoder, fast):
  ChromaDB returns top-5 candidates ──┐
                                      │
Stage 2 (Cross-encoder, accurate):    │
  Score each (query, candidate) pair   │
  Return top-3 ────────────────────────┘
```

This is the **standard production pattern** used by:
- **Glean** — enterprise search
- **Notion AI** — Q&A over notes
- **Perplexity** — answer engine
- **Cohere Rerank** — API service

### Why both?

The bi-encoder is like a **librarian** who knows which aisle each book is in.
The cross-encoder is like a **reviewer** who reads the first page of each candidate.

Librarian is fast — narrows 10,000 books to 50 candidates.
Reviewer is thorough — picks the best 3 from those 50.

### Score interpretation

The cross-encoder returns a relevance score (not normalized). The absolute value doesn't matter — only the relative ranking. Scores are shown in the UI for transparency.

---

## 6. Query Rewriting (`rag.py`)

### The problem

```
User: "Who is Gol D. Roger?"
Assistant: "He was the Pirate King..."
User: "What was his bounty?"       ← "his" refers to Roger
```

Without rewriting, the vector search for `"What was his bounty?"` would find chunks about random characters with the word "his". Rewriting resolves the pronoun:

```
Rewrite: "What was Gol D. Roger's bounty?"
Search:  finds "Gol D. Roger had a bounty of 5,564,800,000 Berries"
```

### How it works

1. Take the last N turns of conversation history
2. Ask the LLM to rewrite the latest question as standalone
3. Use the rewritten query for vector search

### When to skip

If there's no history, rewriting is skipped — the original question is already standalone.

---

## 7. LLM Generation (`rag.py`)

### The prompt template

```
You are a knowledgeable One Piece scholar. Answer using ONLY the context.
If the context doesn't contain enough information, say so.
When you use information from a source, cite it as [Source 1], [Source 2], etc.

Context:
[Source 1] Luffy ate the Gomu Gomu no Mi...
[Source 2] The Gomu Gomu no Mi is a Paramecia-type...

Question: What is Luffy's Devil Fruit?

Answer:
```

Key design choices:
- **Role assignment** ("One Piece scholar") guides tone and focus
- **"ONLY the context"** prevents hallucination
- **Source citations** enable verification
- **"If you don't know"** provides graceful degradation

### Why not just ask the LLM directly?

Without RAG, the LLM relies on its training data — which may be outdated, incomplete, or wrong. RAG grounds the answer in **retrieved evidence** that you control.

---

## 8. Streamlit UI (`app.py`)

### State management

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
```

Streamlit re-runs the script on every interaction. `st.session_state` persists across runs — without it, chat history would reset on every message.

### The chat loop

1. User sends message → stored in `st.session_state.messages`
2. `rag.ask()` runs the full pipeline
3. Result displayed with expandable source chunks
4. Both query and response appended to `st.session_state.history` for rewriting
5. History trimmed to last 10 turns to prevent context overflow

### Sidebar as control panel

The sidebar is deliberately kept separate from the chat — it manages **data infrastructure** (scrape, index, clear), while the main panel manages **conversation** (ask, answer, cite).

---

## 9. Model Architecture Cheat Sheet

| Component | Model | Size | Speed |
|-----------|-------|------|-------|
| Embeddings | `all-MiniLM-L6-v2` | 80MB | 10K docs/sec |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` | 80MB | 50 pairs/sec |
| LLM | `llama2` (via Ollama) | 4GB | 20 tokens/sec |

All run **locally** — no API keys, no cloud costs.

---

## 10. Comparison to Production RAG

| Feature | Poneglyph Reader | Production (Glean/Perplexity) |
|---------|-----------------|-------------------------------|
| Vector DB | ChromaDB (local) | Pinecone / Weaviate (cloud) |
| Embeddings | MiniLM-L6 (local) | OpenAI ada-002 / Cohere embed |
| Reranker | Cross-encoder (local) | Cohere Rerank / custom model |
| LLM | Llama 2 (local) | GPT-4 / Claude (cloud) |
| Search | Dense vector only | Hybrid (dense + sparse BM25) |
| Scaling | Single machine | Distributed, sharded |
| Monitoring | None | LangSmith / custom tracing |

The **architecture is the same** — only the components scale up.

---

## Forward References

- **LangChain LCEL** (`7-Advanced-Frameworks/01-langchain-basics.py`): Replace manual pipeline with `prompt | model | parser`
- **LangGraph StateGraph** (`7-Advanced-Frameworks/03-langgraph-workflows.py`): Model the pipeline as a graph with conditional routing
- **LangSmith Tracing** (`7-Advanced-Frameworks/05-langsmith-monitoring.py`): Add observability to see every retrieval and generation
- **Guardrails** (`7-Advanced-Frameworks/06-guardrails-validation.py`): Validate LLM outputs against Pydantic schemas
- **Advanced Patterns** (`7-Advanced-Frameworks/08-advanced-patterns.py`): Multi-LLM routing, embedding cache, fallback chains
