# Phase 4 — NLP + Transformers

## The Progression of Text Representations

**TF-IDF (Term Frequency — Inverse Document Frequency):** Sparse vector where each dimension is a word, weighted by how often it appears in a document vs across the corpus. No notion of meaning — "rubber man" and "stretchy pirate" have zero similarity. Fast, interpretable, good baseline for text classification on small data. O(vocab_size) memory.

**Word2Vec (word embeddings):** Dense vectors (typically 50-300 dimensions) learned by predicting a word from its context (CBOW) or context from a word (skip-gram). Captures some semantic relationships: `king - man + woman ≈ queen`. But one fixed vector per word — "bank" (river) and "bank" (money) share the same embedding.

**Contextual embeddings (BERT, transformers):** The same word gets different vectors depending on surrounding context. "Bank" in "river bank" vs "money bank" produce different embeddings. This is what powers modern NLP and RAG. ~768 dimensions for BERT-base, ~384 for MiniLM.

**Why this order matters:** Each step fixes a limitation of the previous one. TF-IDF has no semantics → Word2Vec adds semantics but no context → BERT adds context. Interviewers ask about this progression.

## Transformer Architecture

**The core insight:** Attention lets every token look at every other token directly, avoiding the sequential bottleneck of RNNs. This is both the power (long-range dependencies) and the weakness (O(n²) compute in sequence length).

**Components:**
- **Token embeddings** + **positional encoding** — since attention has no inherent sense of order, positional signals (sinusoidal or learned) are added to tell the model where each token is.
- **Self-attention (Q, K, V):** Each token produces a Query, Key, and Value vector. Query vs Key dot products determine attention weights (which tokens matter to each other). Values are combined weighted by those attention scores.
- **Multi-head attention:** Multiple attention mechanisms in parallel, each learning to focus on different relationships (syntax, coreference, semantics). Results are concatenated and projected back.
- **Feed-forward network:** A simple MLP applied per token. Adds non-linear transformation capacity.
- **Layer normalization + residual connections:** Stabilize training and allow gradients to flow through many layers.

**Encoder vs Decoder:**
- **Encoder-only (BERT):** Bidirectional attention — each token sees all other tokens. Best for understanding tasks: classification, NER, embedding extraction.
- **Decoder-only (GPT):** Causal (masked) attention — each token only sees itself and previous tokens. Best for generation: text completion, chat, code generation.
- **Encoder-decoder (T5):** Encoder processes input, decoder generates output with cross-attention to encoder. Best for sequence-to-sequence: translation, summarization.

## Tokenization

**BPE (Byte-Pair Encoding):** Starts with individual characters, iteratively merges the most frequent pairs. Handles rare/unknown words by breaking them into subword units. GPT uses BPE.

**WordPiece:** Similar to BPE but merges based on likelihood rather than frequency. BERT uses WordPiece.

**SentencePiece:** Works on raw text without spaces — useful for languages without clear word boundaries. Used by Llama, T5.

**Why tokenization matters:** The same text can be tokenized very differently by different tokenizers, affecting both cost (API pricing is per token) and model understanding.

## Fine-Tuning

- **Full fine-tuning:** Update all parameters on task data. Best quality, most expensive. Requires a GPU for anything beyond tiny models.
- **LoRA (Low-Rank Adaptation):** Train small rank-decomposition matrices injected into attention layers. Only ~0.1-1% of parameters are trained. The base model stays frozen. This is the standard approach for fine-tuning LLMs on consumer hardware.
- **QLoRA:** LoRA + 4-bit quantization of the base model. Fine-tune a 7B model on 24GB GPU. The practical standard for open-source LLM fine-tuning.

**When to fine-tune vs prompt:**
- Fine-tune: high-volume narrow task with labeled data, need reliability, can afford the upfront cost.
- Prompt/few-shot: exploratory, data-scarce, frequent task changes, can't afford fine-tuning infra.

## Evaluation Metrics for NLP

- **Perplexity:** How "surprised" the model is by the text — lower is better for generation. Not directly comparable across tokenizers.
- **BLEU:** N-gram overlap between generated and reference text. Used for translation. Correlates poorly with human judgment for creative tasks.
- **ROUGE:** Recall-oriented overlap (how many reference n-grams appear in the output). Used for summarization.
- **BERTScore:** Embedding-based similarity between generated and reference text. Better correlation with human judgment.

## Interview Must-Knows

- TF-IDF → Word2Vec → BERT progression: what each adds, limitations of each.
- Self-attention in one sentence: each token computes relevance weights to every other token and pulls information accordingly.
- Why multi-head attention: different heads specialize in different relationships.
- Why positional encoding: attention has no sequential order, so position must be injected explicitly.
- Encoder vs decoder vs encoder-decoder: which architecture for which task.
- BPE vs WordPiece vs SentencePiece: how they differ and why it matters.
- Why transformers are O(n²): every token attends to every other token.
- LoRA vs full fine-tuning: tradeoff between quality and cost.
- When to fine-tune vs prompt.
- Attention is all you need — know the paper title and the basic architecture diagram.
