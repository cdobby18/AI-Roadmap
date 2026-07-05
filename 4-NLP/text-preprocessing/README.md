# 1 · Text Preprocessing

Before any model sees text, it has to become numbers. Tokenization is the first — and most underrated — step in every NLP and LLM pipeline: it decides how many "units" your text costs and what the model can even see.

---

## Progress Checklist

- [x] `textPipeline.py` — full BERT tokenizer pipeline: padding, truncation, attention masks, batch tokenization
- [x] `tokenization.py` — GPT-2 tokenizer: tokenize/encode/decode, BPE subword splitting on rare/compound words

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `tokenizer(text)` | Turns raw text into `input_ids` + `attention_mask` the model can consume |
| `padding="max_length"` | Pads shorter sequences so a batch has uniform shape |
| `attention_mask` | 1 for real tokens, 0 for padding — tells the model what to ignore |
| BPE (byte-pair encoding) | Splits rare/compound words into subwords (e.g. `superintelligence` → multiple pieces) — keeps vocab size manageable while still handling unseen words |
| `tokenizer.decode(ids)` | Reverses tokenization — useful for sanity-checking what the model actually sees |
| Token count | Directly drives LLM latency and API cost — more tokens = more $$$ |

---

## Gotcha

Different models use different tokenizers (BERT's WordPiece vs GPT-2's BPE) — the same sentence produces different token counts and IDs depending on which one you load. Always tokenize with the tokenizer that matches your model.
