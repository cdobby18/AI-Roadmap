# 4 · Pre-trained Models

Standing on the shoulders of models already trained on billions of tokens — fine-tune BERT for a task, generate text with GPT-2, and ship the result to the Hugging Face Hub.

---

## Progress Checklist

- [x] `bert-classification.py` — fine-tune `bert-base-uncased` for sentiment classification with `Trainer` + `TrainingArguments` on a small `Dataset`, then run inference on new text
- [x] `gpt-text-generation.py` — `pipeline("text-generation")` with GPT-2: greedy vs sampled decoding, `temperature`/`top_k` effects, plus a manual look at next-token logits → softmax → top-5 predictions
- [x] `push-to-hub.py` — upload a fine-tuned model + tokenizer to the Hugging Face Hub so it can be loaded by name anywhere

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `Trainer` / `TrainingArguments` | Hugging Face's training loop wrapper — handles batching, eval, logging so you don't write the loop by hand |
| Fine-tuning | Continue training a pre-trained model on task-specific labeled data — worth it for narrow, high-volume tasks |
| `do_sample=False` (greedy) | Always picks the most likely next token — deterministic, can be repetitive |
| `temperature` | <1 = more deterministic/focused, >1 = more random/creative; 1.0 = default |
| `top_k` | Restricts sampling to the k most likely next tokens at each step |
| Autoregressive generation | GPT predicts one token at a time, appends it, and repeats — each call only ever predicts the *next* token |
| `push_to_hub()` | Versions and shares a model/tokenizer so `pipeline(model="you/model-name")` works from anywhere |

---

## Gotcha

`bert-classification.py` trains on only 6 examples — enough to prove the mechanics work, not enough to generalize. In a real fine-tune you'd want hundreds to thousands of labeled examples per class.
