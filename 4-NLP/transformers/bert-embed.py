from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


def mean_pool(last_hidden_state, attention_mask):
    # Average token embeddings, ignoring padding tokens (where mask == 0)
    mask = attention_mask.unsqueeze(-1).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)


def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return mean_pool(outputs.last_hidden_state, inputs["attention_mask"])


tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

# --- Shape of BERT output ---
text = "AI is transforming the world"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

print("last_hidden_state shape:", outputs.last_hidden_state.shape)
# (batch=1, seq_len, hidden_dim=768) — one 768-d vector per token

# CLS token (position 0) was designed for classification tasks
cls_embedding = outputs.last_hidden_state[0, 0, :]
print("CLS embedding shape:", cls_embedding.shape)  # (768,)

# Mean pooling averages all tokens — generally better than CLS for semantic similarity
mean_embedding = mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
print("Mean pool embedding shape:", mean_embedding.shape)  # (1, 768)

print()

# --- Cosine similarity between sentences ---
# This is the foundation of semantic search and RAG retrieval
sentences = [
    "A pirate who wants to find the legendary treasure.",
    "A swordsman with three swords who trains to become the world's greatest.",
    "A navigator who draws sea charts and loves money.",
    "A man searching for a vast ocean of treasure called the One Piece.",
]

embeddings = torch.cat([get_embedding(s, tokenizer, model) for s in sentences])
embeddings = F.normalize(embeddings, dim=-1)   # unit vectors → cosine sim = dot product

print("Cosine similarity matrix:")
sim_matrix = embeddings @ embeddings.T
for i, s in enumerate(sentences):
    print(f"\n  '{s[:50]}'")
    for j, score in enumerate(sim_matrix[i]):
        if i != j:
            print(f"    vs '{sentences[j][:45]}...' → {score.item():.3f}")

# Notice: sentence 0 and 3 are semantically close (both about treasure/One Piece)
# even though they share few exact words — that's what embeddings capture.
