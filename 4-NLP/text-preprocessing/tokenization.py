from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "Natural Language Processing is amazing!"
tokens = tokenizer.tokenize(text)
token_ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Token IDs:", token_ids)
print("Token count:", len(token_ids))

decoded = tokenizer.decode(token_ids)
print("Decoded:", decoded)

# BPE splits rare/compound words into subwords — this is how LLMs see text
text2 = "ChatGPT is an extraordinary superintelligence"
tokens2 = tokenizer.tokenize(text2)
print("\nSubword tokens:", tokens2)
