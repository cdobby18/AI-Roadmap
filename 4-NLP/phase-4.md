# Phase 4 · NLP + Transformers

**Prerequisite:** Phase 3 (ML)  
**Next:** Phase 5 (LLMs)

This phase has two parts: understanding NLP concepts historically, then understanding transformers architecturally. You need both — the history tells you *why* transformers won; the architecture tells you *how* they work.

---

## Folder Priorities

| Folder | What | Priority |
|--------|------|----------|
| `text-preprocessing/` | Tokenization, text pipeline | Skim — modern models handle this |
| `text-representation/` | TF-IDF, Word2Vec, embeddings | Required — understand *why* embeddings replaced TF-IDF |
| `nlp-applications/` | NER, sentiment, summarization via HuggingFace | Required |
| `pre-trained-models/` | BERT classification, GPT generation, HF pipeline | Required |
| `transformers/` | Attention mechanism, BERT embeddings, transformer class | Required |

---

## What You'll Learn

### NLP Foundations
- **Tokenization** — LLMs read tokens, not words. Understand byte-pair encoding (BPE) and why it matters for context windows and cost.
- **Word Embeddings** — words as vectors, semantic similarity, Word2Vec intuition. Foundation of how models understand meaning.
- **TF-IDF** — understand it so you know why embeddings replaced it. The contrast is the lesson.
- **Encoder vs Decoder** — know this cold. BERT = encoder (bidirectional, understanding). GPT = decoder (causal, generation). Comes up in every AI interview.

### Transformers — How They Actually Work
- **The Attention Mechanism** — queries, keys, values. Attention is the model deciding *what to focus on* when processing each token.
- **Scaled Dot-Product Attention** — why scores are scaled by `√d_k`. This is a real interview question.
- **Multi-Head Attention** — why one attention head isn't enough. Each head learns a different type of relationship.
- **Positional Encoding** — transformers have no built-in sense of order. Understand how position is injected.
- **The Transformer Block** — attention → add & norm → feed-forward → add & norm. Know this sequence.
- **What Fine-Tuning Actually Does** — you're adjusting weights that already encode language understanding, not training from scratch.

### Practical Skills
- **HuggingFace `pipeline()`** — run NER, summarization, sentiment, QA in 3 lines. Know which architecture fits which task.
- **Fine-tuning BERT** — use `Trainer` API on a classification task. This is the pattern for every fine-tune job.
- **HuggingFace Hub** — push your fine-tuned model. Real engineers publish their work.

---

## Progress Checklist

### Text Representation (Required)
- [ ] `text-representation/word2vec.py` — word vectors, semantic similarity
- [ ] `text-representation/wordEmbed.py` — embedding layer intuition
- [ ] `text-representation/tfidf.py` — TF-IDF from scratch, then understand why it's limited

### NLP Applications (Required)
- [ ] `nlp-applications/sentiment-analysis.py`
- [ ] `nlp-applications/NER.py`
- [ ] `nlp-applications/text-summarization.py`

### Pre-Trained Models (Required)
- [ ] `pre-trained-models/bert-classification.py` — fine-tune BERT with Trainer API on a real dataset
- [ ] `pre-trained-models/gpt-text-generation.py` — GPT generation
- [ ] `pre-trained-models/push-to-hub.py` — publish your fine-tuned model to HuggingFace Hub

### Transformers (Required)
- [ ] `transformers/attention-mech.py` — implement scaled dot-product attention from scratch in PyTorch
- [ ] `transformers/transformers-basic.py` — build a full transformer block (attention → add & norm → FF → add & norm)
- [ ] `transformers/simple-transform-class.py` — encoder vs decoder: BERT (bidirectional) vs GPT (causal)
- [ ] `transformers/bert-embed.py` — extract BERT embeddings (foundation of RAG)

### Text Preprocessing (Skim)
- [ ] `text-preprocessing/tokenization.py`
- [ ] `text-preprocessing/textPipeline.py`

---

## Resources

| Resource | What You Get | Format | Cost |
|----------|-------------|--------|------|
| Jay Alammar — "The Illustrated Transformer" | The single best visual explanation of transformers. Required reading. | Blog | Free |
| Andrej Karpathy — "Let's build GPT from scratch" (YouTube) | Build a GPT character-level model from scratch in PyTorch. Watch every minute. | Video | Free |
| 3Blue1Brown — "Attention in transformers" (YouTube) | Best visual intuition for attention. Watch before reading papers. | Video | Free |
| HuggingFace NLP Course (huggingface.co/learn) | The definitive NLP + Transformers course. Chapters 1–4 are required. | Interactive | Free |
| Jay Alammar — "The Illustrated Word2Vec" | Best visual explanation of embeddings. | Blog | Free |
| Jay Alammar — "The Illustrated BERT" | Understand BERT architecturally before fine-tuning it. | Blog | Free |
| Andrej Karpathy — "Let's build the GPT tokenizer" (YouTube) | 2-hour deep dive on tokenization. Watch it once. | Video | Free |
| "Attention Is All You Need" (original paper) | Read the abstract, intro, and architecture section. Not the full paper — yet. | Paper | Free |
| HuggingFace Trainer docs | Official reference for fine-tuning. Bookmark it. | Docs | Free |

---
