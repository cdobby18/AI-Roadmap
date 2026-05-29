import torch
import torch.nn as nn

vocab_size = 10
embedding_dim = 4

embedding = nn.Embedding(vocab_size, embedding_dim)

token_ids = torch.tensor([1, 2, 3])
vectors = embedding(token_ids)

print("Token IDs:", token_ids)
print("Embedding vectors:\n", vectors)
print("Shape:", vectors.shape)

# Each token ID maps to a learnable vector updated during training.
# This is the same mechanism transformers use internally.
