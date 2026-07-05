# Phase 4 · NLP + Transformers

This phase takes you from raw text to the architecture behind every modern LLM: preprocessing, classic word representations, attention from scratch, and using pre-trained transformers for real tasks.

**Prerequisite:** Phase 3 (Machine Learning)
**Next:** Phase 5 (LLMs)

---

## Structure

| Folder | Topic | Priority |
|--------|-------|----------|
| `text-preprocessing/` | Tokenization (BERT WordPiece, GPT-2 BPE) | Required |
| `text-representation/` | TF-IDF, word2vec, embedding lookup tables | Required |
| `transformers/` | Attention, multi-head attention, positional encoding, encoder vs decoder | Required |
| `pre-trained-models/` | Fine-tuning BERT, GPT-2 generation, Hugging Face Hub | Required |
| `nlp-applications/` | Sentiment analysis, NER, summarization, simple chatbot | Required |

---

## What AI Engineers Actually Need Here

Every section here is daily-use. Tokenization determines LLM cost/latency, embeddings are the foundation of search/RAG, and attention mechanics come up constantly in interviews ("explain how attention works without the math" is a classic). Don't skip the from-scratch attention files (`transformers/attention-mech.py`, `multi-head-attention.py`) even though `pipeline()` makes it easy to never think about them — interviewers will ask you to explain what's happening inside the black box.

---

## Master Progress Checklist

### 1 · Text Preprocessing
- [x] BERT tokenizer pipeline: padding, truncation, attention masks, batching
- [x] GPT-2 tokenizer: tokenize/encode/decode, BPE subword splitting

### 2 · Text Representation
- [x] TF-IDF (sparse, count-based)
- [x] word2vec (dense, static, CBOW/skip-gram)
- [x] `nn.Embedding` lookup table

### 3 · Transformers
- [x] Scaled dot-product attention from scratch
- [x] Multi-head attention from scratch + causal masking
- [x] Sinusoidal positional encoding
- [x] Full encoder `TransformerBlock` (attention + LayerNorm + FFN)
- [x] Encoder (BERT) vs decoder (GPT-2) comparison
- [x] BERT embeddings: CLS vs mean pooling, cosine similarity semantic search

### 4 · Pre-trained Models
- [x] Fine-tune BERT for classification (`Trainer` + `TrainingArguments`)
- [x] GPT-2 text generation: greedy vs sampling, temperature, top_k
- [x] Push a fine-tuned model to the Hugging Face Hub

### 5 · NLP Applications
- [x] Sentiment analysis (single + batch)
- [x] Named Entity Recognition
- [x] Text summarization
- [x] Simple chatbot (prompt continuation)

---

## Learning Path

```
text-preprocessing → text-representation → transformers → pre-trained-models → nlp-applications
```

Preprocessing and representation build the "how does text become numbers" intuition. Transformers build the architecture from scratch so it isn't a black box. Pre-trained-models and nlp-applications then show the payoff: the same concepts, used in three lines via `pipeline()`.

---

## Resources

| Resource | What | Format | Cost |
|----------|------|--------|------|
| Hugging Face — NLP Course | Best free deep dive on tokenizers, transformers, fine-tuning | Docs + Notebooks | Free |
| Jay Alammar — The Illustrated Transformer | The canonical visual explanation of attention | Blog | Free |
| Hugging Face — Pipeline tutorial | Pre-trained models in one call | Docs | Free |
| gensim — Word2Vec docs | CBOW vs skip-gram, API reference | Docs | Free |
| Hugging Face Hub docs | `push_to_hub`, model versioning | Docs | Free |

---

## Capstone Project

**[Vivre Card](../8-Projects/phase-4-vivre-card/)** — A semantic character search engine: describe a One Piece character in your own words and BERT returns the closest matches by meaning, not keyword.

Applies the phase end-to-end: `data.py` (25 character bios) → `embeddings.py` (BERT + mean pooling + L2-normalize, cached to `embeddings.pt`) → `search.py` (cosine similarity ranking via a single matrix multiply) → `app.py` (Gradio UI). It's also a direct preview of Phase 6's RAG pipeline — the embed-query → cosine-search steps are identical, just at 25 characters instead of 10,000 document chunks.
