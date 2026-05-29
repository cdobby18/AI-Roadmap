from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import torch

text = "AI engineering is the future"

# --- Encoder (BERT-style) ---
# Bidirectional: each token attends to all other tokens.
# Best for: classification, NER, embeddings, understanding tasks.
enc_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
enc_model = AutoModel.from_pretrained("bert-base-uncased")

enc_inputs = enc_tokenizer(text, return_tensors="pt")
with torch.no_grad():
    enc_output = enc_model(**enc_inputs)

print("Encoder (BERT)")
print("  Hidden states shape:", enc_output.last_hidden_state.shape)
# (batch, seq_len, hidden_dim) — one vector per token, context from both directions


# --- Decoder (GPT-style) ---
# Causal/unidirectional: each token only attends to previous tokens.
# Best for: text generation, chat, completion tasks.
dec_tokenizer = AutoTokenizer.from_pretrained("gpt2")
dec_model = AutoModelForCausalLM.from_pretrained("gpt2")

dec_inputs = dec_tokenizer(text, return_tensors="pt")
with torch.no_grad():
    dec_output = dec_model(**dec_inputs)

print("\nDecoder (GPT-2)")
print("  Logits shape:", dec_output.logits.shape)
# (batch, seq_len, vocab_size) — next-token probability distribution at each position
