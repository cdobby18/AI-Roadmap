from transformers import AutoTokenizer

# BERT tokenizer — handles padding, truncation, and attention masks automatically
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "AI engineering requires understanding transformers and embeddings."

encoded = tokenizer(
    text,
    padding="max_length",
    truncation=True,
    max_length=20,
    return_tensors="pt",
)

print("Input IDs:     ", encoded["input_ids"])
print("Attention mask:", encoded["attention_mask"])
print("Decoded:       ", tokenizer.decode(encoded["input_ids"][0]))

# Batch tokenization — how you'd process a dataset before fine-tuning
texts = ["AI is transforming the world.", "PyTorch is the standard for LLM work."]
batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
print("\nBatch input IDs shape:", batch["input_ids"].shape)
