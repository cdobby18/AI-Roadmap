# Vivre Card — Context

**Phase:** 4 — NLP + Transformers + Pre-trained Models
**Theme:** A semantic character search engine — describe a One Piece character in your own words and BERT returns the closest matches by meaning, not keyword.

---

## What This Builds

Describe a character — *"a rubber man who wants to be king of the pirates"* — and BERT returns the most semantically similar characters from a set of 25 bios, ranked by cosine similarity. This is the exact same mechanism that powers RAG retrieval in Phase 6, just with 25 characters instead of 10,000 document chunks.

---

## Files

| File | What It Does |
|---|---|
| `data.py` | 25 One Piece characters with descriptive bios (deliberately written without naming abilities by their in-universe name, so matches are genuinely semantic) |
| `embeddings.py` | Loads BERT, embeds all bios via mean pooling, L2-normalizes, saves `embeddings.pt` |
| `search.py` | Loads the saved index, embeds a query, ranks by cosine similarity, returns top-k |
| `app.py` | Gradio UI — text box in, ranked results with similarity bars out |

---

## How to Run

```bash
pip install torch transformers gradio

python embeddings.py   # generate embeddings.pt (~30s on CPU, run once)
python search.py       # test search in the terminal
python app.py          # Gradio UI → http://localhost:7860
```

---

## The Core Pipeline

**1 — Embed the database (offline, once)**
```
character bio text → BERT → 768-dim vector → mean pool → L2-normalize → save (embeddings.pt)
```

**2 — Embed the query (online, per request)**
```
user query → BERT → 768-dim vector → mean pool → L2-normalize
```

**3 — Score and rank**
```
cosine_similarity = query_vector · bio_vector   (dot product of unit vectors)
sort descending → return top-k
```

`search.py` computes all 25 scores at once as a single matrix multiplication (`query_embedding @ embeddings.T`).

---

## Mean Pooling vs CLS Token

BERT outputs one 768-dim vector per token. To get a single sentence embedding:

- **CLS token** (position 0) — designed for classification fine-tuning, underperforms for raw similarity.
- **Mean pooling** — average all non-padding tokens, weighted by the attention mask. This is what the project uses.

```python
def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)
```

`attention_mask` is 1 for real tokens and 0 for padding — multiplying by it before averaging keeps padding from diluting the sentence vector.

---

## Model

`bert-base-uncased` (768-dim output), loaded once at startup in each script (`embeddings.py`, `search.py`, `app.py`) — never per-request. Embeddings are precomputed and cached to `embeddings.pt`; only the query is embedded live.
