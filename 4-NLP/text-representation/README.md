# 2 · Text Representation

Three ways to turn words into numbers, in increasing order of "understanding meaning": sparse counting (TF-IDF), static dense vectors (word2vec), and a learnable lookup table (`nn.Embedding`) — the same building block transformers use internally.

---

## Progress Checklist

- [x] `tfidf.py` — `TfidfVectorizer` on a 3-sentence corpus: sparse, count-based vectors, no notion of meaning
- [x] `word2vec.py` — `gensim.Word2Vec`, CBOW by default (predicts a word from its context): dense, fixed vector per word
- [x] `wordEmbed.py` — `nn.Embedding` lookup table: token ID → learnable dense vector, updated during training

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| TF-IDF | Scores words common in one document but rare across the corpus — sparse, fast, zero semantics |
| word2vec (CBOW) | Predicts the center word from surrounding context words — the reverse of skip-gram |
| word2vec (skip-gram) | Predicts context words from a center word — set `sg=1` in gensim (this repo's `word2vec.py` uses the CBOW default, `sg=0`) |
| Static embedding | One fixed vector per word regardless of sentence — "bank" (river) and "bank" (money) get the same vector |
| `nn.Embedding(vocab_size, dim)` | A trainable matrix — row `i` is the vector for token `i`; gradients update it during training |

---

## The Progression (interview-ready)

TF-IDF (sparse counting) → word2vec (dense, static, some semantics) → transformer embeddings (dense, contextual — see `../transformers/`). Knowing where each fits, not "transformers are always better," is the actual skill.
