# Poneglyph Reader — HuggingFace Spaces Deployment

One-click deploy of the One Piece RAG chat app to HuggingFace Spaces.

---

## Quick Deploy (2 minutes)

### Option 1: Via HF Hub GUI

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Space name: `poneglyph-reader`
3. License: MIT
4. SDK: **Streamlit**
5. Click **Create Space**

Then push the code:

```bash
# From repo root
git remote add hf https://huggingface.co/spaces/<YOUR_USERNAME>/poneglyph-reader
git subtree push --prefix Projects/phase-6-poneglyph hf main
```

### Option 2: Via Docker (SDK: Docker)

1. Create a Space with **Docker** SDK
2. Upload the `Dockerfile` from `8-Deploy/`
3. Space builds and runs automatically

---

## Setting Up the LLM Backend

Ollama isn't available on HF Spaces. The app uses **HuggingFace Inference API** instead:

1. Get a free HF token: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Add it as a Space secret:
   - Go to your Space → **Settings** → **Repository Secrets**
   - Add `HF_TOKEN` = your token

Without a token, the app still works — it falls back to a no-LLM mode (retrieval only).

---

## Files to Copy

To deploy the Poneglyph Reader to HF Spaces, you need these files from `Projects/phase-6-poneglyph/`:

```
app.py
config.py
rag.py
ingestion.py
scraper.py
requirements.txt
data/                    # Pre-built ChromaDB (optional — app rebuilds on first run)
```

Plus this Space metadata:

```
README.md         (this file — becomes the Space homepage)
.gitattributes
```

---

## Cost

**Free tier:** 16GB storage, 2 vCPUs, ~$0/month.
**Upgrade:** $0.60/hr for CPU upgrade, $0.90/hr for GPU (A10G).
The Poneglyph Reader runs fine on the free tier. The sentence-transformers model loads in ~5s on first request.

---

## Architecture

```
User → HF Spaces (Streamlit) → ChromaDB (persistent) → HF Inference API (LLM)
                                         ↑
                              sentence-transformers (embeddings + reranker)
```
