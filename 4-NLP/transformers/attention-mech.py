import torch
import torch.nn.functional as F
import math


def scaled_dot_product_attention(Q, K, V):
    d_k = Q.shape[-1]
    # Score each query against every key, scale to prevent vanishing gradients
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights


# batch=1, sequence_length=4, embedding_dim=8
Q = torch.rand(1, 4, 8)
K = torch.rand(1, 4, 8)
V = torch.rand(1, 4, 8)

output, weights = scaled_dot_product_attention(Q, K, V)

print("Output shape:", output.shape)     # (1, 4, 8)
print("Attention weights:\n", weights)   # which tokens attend to which
