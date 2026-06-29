# Phase 4 Project — Vivre Card

**Theme:** One Piece  
**Phase:** 4 — NLP + Transformers + Pre-trained Models  
**Prereqs:** Phase 1 (Python + OOP) · Phase 2 (FastAPI) · Phase 3 (ML + PyTorch)

---

## What This Project Builds

A semantic character search engine. You describe a One Piece character in your own words — "a rubber man who wants to be king of the pirates" — and BERT returns the most semantically similar characters from its embeddings, ranked by cosine similarity.

This is the exact same concept powering RAG retrieval in Phase 6, just with 25 characters instead of 10,000 document chunks.

---

## Project Files

| File | What it does | Phase 4 skill |
|------|--------------|---------------|
| `data.py` | 25 One Piece characters with descriptive bios | Python data structuring |
| `embeddings.py` | Loads BERT, embeds all bios, saves `embeddings.pt` | BERT embeddings, mean pooling, `torch.save` |
| `search.py` | Loads index, embeds query, returns top-k by cosine similarity | Cosine similarity, vector search |
| `app.py` | Gradio UI — text input, similarity bar, bio output | Gradio, model inference |

---

## How to Run

```bash
# 1. Install dependencies (one-time)
pip install torch transformers gradio

# 2. Generate embeddings (run once — takes ~30 seconds on CPU)
python embeddings.py

# 3. Test search in the terminal
python search.py

# 4. Launch the Gradio UI
python app.py
# → Opens at http://localhost:7860
```

---

## The Core Concept: Semantic Search

**Step 1 — Embed the database (offline, once)**
```
character bio text → BERT → 768-dimensional vector → normalize → save
```

**Step 2 — Embed the query (online, per request)**
```
user query → BERT → 768-dimensional vector → normalize
```

**Step 3 — Score and rank**
```
cosine_similarity = query_vector · bio_vector   (dot product of unit vectors)
sort descending → return top-k
```

**Why cosine similarity?**
After L2 normalization, the dot product equals cosine similarity. The angle between two vectors measures semantic relatedness — "rubber man wants to be pirate king" and "stretchy pirate captain who wants to find the legendary treasure" will be close in embedding space even with zero word overlap.

---

## Mean Pooling vs CLS Token

BERT outputs one 768-d vector per token. To get a single sentence embedding:

- **CLS token** — position 0, designed for classification. Works for fine-tuning but underperforms for similarity.
- **Mean pooling** — average all non-padding tokens. Better for semantic search. This project uses mean pooling.

```python
def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)
```

The `attention_mask` is 1 for real tokens and 0 for padding — multiplying by it prevents padding tokens from affecting the average.

---

## Study Notes

### Why This is the Foundation of RAG

In Phase 6, the pipeline is:
1. Ingest documents → chunk → embed → store in ChromaDB
2. User query → embed → cosine search against ChromaDB → retrieve top-k chunks
3. Chunks + query → LLM → answer

Steps 2 and 3 here (embed query → cosine search) are **identical** to what you built in this project. The only difference in RAG is the database scale and a final LLM generation step on top.

### What BERT Embeddings Actually Capture

When you search "someone who controls fire and is related to the pirate king", BERT returns Portgas D. Ace. It didn't match "fire" → "Flame-Flame Devil Fruit" as a keyword — it matched the semantic relationship between those concepts in embedding space.

This works because BERT was pre-trained on billions of text tokens and learned that flame, fire, fire powers, and burning share similar contexts. Fine-tuned retrieval models (like `sentence-transformers`) push this further — but even vanilla BERT is impressive here.

### Cosine Similarity vs Euclidean Distance

Both can measure vector proximity. Cosine similarity is preferred for embeddings because:
- It's scale-invariant — only the direction matters, not the magnitude
- After L2 normalization, cosine sim = dot product = O(n) FLOPS per query
- Most embedding models are trained to push semantically similar texts toward the same direction

### What "L2-normalize" Means

```python
embeddings = F.normalize(embeddings, dim=-1)
```

This divides each vector by its own L2 norm (Euclidean length), turning it into a unit vector. Then:

```
cosine_similarity(a, b) = a · b / (|a| · |b|)
# After normalization: |a| = |b| = 1, so:
cosine_similarity(a, b) = a · b
```

One matrix multiplication against the full character index gives all scores at once.

### Why Not Use TF-IDF Here?

TF-IDF would give zero similarity between "rubber man" and "stretchy pirate captain" — there's no word overlap. That's the entire point of this project: dense embeddings capture meaning; sparse representations capture exact words. By the time you finish Phase 6, you'll know exactly when to use each.

---

## Phase 4 Skills Demonstrated

- [x] BERT embedding extraction (`AutoModel`, `last_hidden_state`)
- [x] Mean pooling — correct handling of padding mask
- [x] L2 normalization — unit vectors for dot-product cosine sim
- [x] Offline index building and saving with `torch.save`
- [x] Query-time embedding and nearest-neighbor retrieval
- [x] Gradio UI with examples, slider control, markdown output
- [x] Model loading at startup, not per-request (production pattern)

---

## Bridge to Phase 6 (RAG)

The next time you build a retrieval system, you'll replace:
- `data.py` → document ingester + chunker
- `embeddings.py` → ChromaDB insert with `collection.add()`
- `search.py` → `collection.query(query_embeddings=..., n_results=k)`
- `app.py` → same Gradio UI + an LLM `generate()` call on the retrieved chunks

The mental model is identical. Only the infrastructure changes.
