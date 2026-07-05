# 5 · NLP Applications

Four common tasks solved in a few lines with Hugging Face `pipeline()` — extraction, classification, generation, and summarization.

---

## Progress Checklist

- [x] `sentiment-analysis.py` — `pipeline("sentiment-analysis")` on single + batch input, with a note on how to read the confidence score
- [x] `NER.py` — `pipeline("ner", aggregation_strategy="simple")`: extract people, organizations, locations from raw text
- [x] `text-summarization.py` — `pipeline("summarization")` to condense a paragraph
- [x] `chatbot-simple.py` — a minimal "chatbot" built from raw `pipeline("text-generation")` continuation on GPT-2

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `pipeline("task")` | One-line inference with a sensible pre-trained default model per task |
| Confidence score | The model's confidence in its *predicted label*, not a general sentiment strength — `NEGATIVE 0.97` means 97% sure it's negative, not "very negative" |
| `aggregation_strategy="simple"` | Merges raw `B-`/`I-` BIO tags into clean entity spans (e.g. `B-PER`+`I-PER` → one `PER` entity) |
| Entity labels | `PER` person, `ORG` organization, `LOC` location, `MISC` everything else |
| Batch inference | Always pass a list to `pipeline()` instead of looping one call at a time |

---

## Gotcha

`chatbot-simple.py` is a naive prompt continuation on raw GPT-2 (`"User: Hello\nBot:"`) — GPT-2 isn't instruction-tuned or conversation-tuned, so it will often continue the pattern incoherently or ramble instead of "replying." A real chatbot needs an instruction/chat-tuned model (or at minimum a chat-formatted prompt template) — this file demonstrates the mechanism, not a usable bot.
