from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# --- Basic generation ---
generator = pipeline("text-generation", model="gpt2")

result = generator("Artificial intelligence will", max_length=40, num_return_sequences=1)
print("Default output:")
print(result[0]["generated_text"])
print()

# --- Generation parameters matter ---
# temperature: controls randomness. 1.0 = default, <1 = more deterministic, >1 = more random
# top_k: at each step, only consider the top-k most likely next tokens
# do_sample: False = greedy (always pick the most likely token), True = sample

prompt = "The future of AI engineering is"

print("Greedy (do_sample=False) — always picks most likely token:")
out = generator(prompt, max_length=50, do_sample=False)
print(out[0]["generated_text"])
print()

print("Low temp (0.3) — focused, repetitive:")
out = generator(prompt, max_length=50, do_sample=True, temperature=0.3, top_k=50)
print(out[0]["generated_text"])
print()

print("High temp (1.5) — creative but sometimes incoherent:")
out = generator(prompt, max_length=50, do_sample=True, temperature=1.5, top_k=50)
print(out[0]["generated_text"])
print()

# --- Token by token: what GPT actually does ---
# At each step, GPT predicts a probability distribution over the full vocabulary.
# It picks one token, appends it, and repeats — this is autoregressive generation.
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()

tokens = tokenizer("The pirate king will", return_tensors="pt")
with torch.no_grad():
    outputs = model(**tokens)

next_token_logits = outputs.logits[0, -1, :]          # logits for the next token
probs = torch.softmax(next_token_logits, dim=-1)
top5 = torch.topk(probs, 5)

print("Top-5 next token predictions:")
for prob, idx in zip(top5.values, top5.indices):
    token = tokenizer.decode([idx.item()])
    print(f"  '{token}' — {prob.item():.2%}")
