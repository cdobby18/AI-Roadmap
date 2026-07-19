# Vivre Card — Lessons

**Phase:** 4 — NLP + Transformers + Pre-trained Models

---

## Why This is the Foundation of RAG

Phase 6's RAG pipeline is: ingest documents → chunk → embed → store in ChromaDB, then user query → embed → cosine search against ChromaDB → retrieve top-k chunks → chunks + query → LLM → answer. The last two steps of that pipeline (embed query → cosine search) are **identical** to what this project builds. The only difference in real RAG is database scale (10,000+ chunks instead of 25 characters) and a final LLM generation step layered on top of retrieval.

## What BERT Embeddings Actually Capture

Searching *"someone who controls fire and is related to the pirate king"* returns Portgas D. Ace — not because "fire" matched "Flame-Flame Devil Fruit" as a keyword, but because BERT matched the semantic relationship between those concepts in embedding space. This works because BERT was pre-trained on billions of tokens and learned that flame, fire, burning, and fire powers share similar contexts — even vanilla `bert-base-uncased` (no fine-tuning) is enough to show this. Fine-tuned retrieval models (`sentence-transformers`) push the same idea further.

## Cosine Similarity vs Euclidean Distance

Cosine similarity is preferred for embeddings because it's scale-invariant (only direction matters, not magnitude), and after L2-normalization it collapses to a single dot product — O(n) per query instead of a full distance computation. Most embedding models are trained to push semantically similar texts toward the same *direction*, which is exactly what cosine similarity measures.

## What "L2-normalize" Means

```python
embeddings = F.normalize(embeddings, dim=-1)
```

Divides each vector by its own Euclidean length, turning it into a unit vector. Once every vector has length 1:

```
cosine_similarity(a, b) = a · b / (|a| · |b|)  →  a · b     (since |a| = |b| = 1)
```

So one matrix multiply against the full index gives every similarity score at once — no separate normalization step needed at query time beyond normalizing the query itself.

## Why Not TF-IDF Here

TF-IDF gives zero similarity between "rubber man" and "stretchy pirate captain" — there's no shared vocabulary. That's the entire point of this project: dense embeddings capture *meaning*, sparse representations (TF-IDF, bag-of-words) capture *exact words*. Knowing which one a task calls for is the actual Phase 4 skill — not "transformers are always better."

---

## Phase 4 Skills Demonstrated

- [x] BERT embedding extraction (`AutoModel`, `last_hidden_state`)
- [x] Mean pooling with correct attention-mask handling
- [x] L2 normalization for dot-product cosine similarity
- [x] Offline index building and persistence (`torch.save`)
- [x] Query-time embedding and nearest-neighbor retrieval
- [x] Gradio UI with examples, a slider control, and markdown output
- [x] Loading the model once at startup, not per-request — the production pattern

---

## Where This Sits in the Roadmap

Phase 3 (`phase-3-bountyhunter`) trained a model *from scratch* on synthetic tabular data; this project instead uses a pre-trained transformer *as-is* — no training loop, no `loss.backward()`. That contrast is the point of Phase 4: understanding when to train a small model from zero versus when to stand on a model that already learned language from billions of tokens.

**Forward reference — Phase 6 (RAG):** the eventual swap is mechanical, not conceptual —
- `data.py` → a document ingester + chunker
- `embeddings.py` → `collection.add()` into ChromaDB
- `search.py` → `collection.query(query_embeddings=..., n_results=k)`
- `app.py` → the same Gradio UI, plus an LLM `generate()` call over the retrieved chunks

The mental model built here (embed → normalize → cosine rank → top-k) carries over unchanged; only the storage and the final generation step are new.
