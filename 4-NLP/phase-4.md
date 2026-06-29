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
- [ ] `transformers/multi-head-attention.py` — implement MHA from scratch with per-head Q/K/V projections and causal masking
- [ ] `transformers/positional-encoding.py` — sinusoidal PE from scratch, visualize wave patterns, understand why it works
- [ ] `transformers/transformers-basic.py` — build a full transformer block (attention → add & norm → FF → add & norm)
- [ ] `transformers/simple-transform-class.py` — encoder vs decoder: BERT (bidirectional) vs GPT (causal)
- [ ] `transformers/bert-embed.py` — extract BERT embeddings, mean pooling, cosine similarity (foundation of RAG)

### Text Preprocessing (Skim)
- [ ] `text-preprocessing/tokenization.py`
- [ ] `text-preprocessing/textPipeline.py`

---

---

## Study Notes

### Things to Know Cold (Interview Level)

**Attention formula — write this from memory:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k) · V
```
- Q = what this token is looking for
- K = what each token offers
- V = the actual information to retrieve
- `√d_k` scaling prevents vanishing gradients when d_k is large (dot products grow with dimension)

**Encoder vs Decoder — single most common interview question:**
| | BERT (Encoder) | GPT (Decoder) |
|---|---|---|
| Attention | Bidirectional — sees all tokens | Causal — sees only past tokens |
| Pre-training | Masked Language Model (MLM) | Next Token Prediction |
| Best for | Classification, NER, embeddings, QA | Text generation, chat, completion |
| Fine-tune task | Add classification head, train | Few-shot or fine-tune on examples |

**Multi-head attention — why multiple heads:**
One attention head learns one type of relationship (e.g. subject-verb). Multiple heads learn different relationships simultaneously (syntax, coreference, proximity). Results are concatenated and projected back to d_model.

**Positional encoding — why it's needed:**
Transformers process all tokens in parallel — unlike RNNs there's no inherent notion of order. Sinusoidal PE is added to the token embedding before the first attention layer. Nearby positions get similar encodings so the model can learn to use distance.

**Fine-tuning vs. training from scratch:**
Fine-tuning adjusts weights that already encode language understanding from pre-training on billions of tokens. You're not teaching the model language — you're redirecting existing knowledge toward your task. That's why fine-tuning on 6 examples can work.

**Tokenization — BPE:**
BERT and GPT don't see words, they see subword tokens. "ChatGPT" might become ["Chat", "G", "PT"]. This lets the vocabulary handle rare and compound words without an out-of-vocabulary problem. Token count ≠ word count — this matters for context window limits and API cost.

**Mean pooling vs CLS token:**
- CLS token: special token prepended to every BERT input, designed to aggregate sequence meaning for classification tasks
- Mean pooling: average of all token embeddings (ignoring padding), generally outperforms CLS for semantic similarity
- For RAG retrieval, mean pooling or sentence-transformers models are standard

---

### Common Mistakes to Avoid

1. **Evaluating on training data** — always split before tokenizing or embedding
2. **Forgetting `model.eval()` and `torch.no_grad()`** during inference — skipping these wastes memory and gives different dropout behavior
3. **Not batching** — calling pipeline() one text at a time is 10–50x slower than batch inference
4. **Confusing `logits` and `probabilities`** — logits are raw scores (can be negative), apply softmax to get probabilities
5. **Using CLS for sentence similarity** — mean pooling works better; for production use `sentence-transformers`

---

### Mental Model: How a Transformer Processes Text

```
Input text
    ↓
Tokenizer → token IDs
    ↓
Token embedding lookup → (seq_len, d_model)
    ↓
+ Positional encoding → (seq_len, d_model)
    ↓
[Transformer Block] × N layers:
    Multi-Head Attention → Add & Norm → Feed-Forward → Add & Norm
    ↓
Output hidden states → (seq_len, d_model)
    ↓
Task head:
    Classification: linear(CLS) → class logits
    Generation: linear(last token) → vocab logits → softmax → next token
```

---

### Bridge to Phase 5 (LLMs)

`bert-embed.py` is the exact same concept behind RAG retrieval. In Phase 6, instead of cosine-searching 4 sentences, you'll cosine-search a vector database of 10,000 document chunks. The math is identical — only the scale changes.

`gpt-text-generation.py` shows autoregressive generation. In Phase 5, you'll control this via system prompts, temperature, and tool calling through the Claude/OpenAI API — same underlying process, different interface.

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
