import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MultiHeadAttention(nn.Module):
    """
    MHA from scratch — no nn.MultiheadAttention used here.
    Each head learns a different type of relationship in the sequence.
    """

    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads   # each head sees a smaller slice of the embedding

        # Separate linear projections for Q, K, V — each head gets different projections
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)   # projects concatenated heads back to d_model

    def split_heads(self, x):
        # (batch, seq, d_model) → (batch, num_heads, seq, d_k)
        batch, seq, _ = x.shape
        x = x.view(batch, seq, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def forward(self, Q, K, V, mask=None):
        # Project then split into heads
        Q = self.split_heads(self.W_q(Q))   # (batch, heads, seq, d_k)
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))

        # Scaled dot-product attention — same as attention-mech.py, applied per head
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            # mask=0 means "don't attend here" — used for padding or causal masking
            scores = scores.masked_fill(mask == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1)

        out = torch.matmul(weights, V)   # (batch, heads, seq, d_k)

        # Merge heads: (batch, heads, seq, d_k) → (batch, seq, d_model)
        batch, _, seq, _ = out.shape
        out = out.transpose(1, 2).contiguous().view(batch, seq, self.d_model)

        return self.W_o(out), weights


# d_model=64, 4 heads → each head attends over 16 dimensions independently
mha = MultiHeadAttention(d_model=64, num_heads=4)

x = torch.rand(1, 10, 64)   # batch=1, seq_len=10, d_model=64
out, weights = mha(x, x, x)  # self-attention: Q=K=V=x

print("Output shape: ", out.shape)      # (1, 10, 64) — same shape as input
print("Weight shape: ", weights.shape)  # (1, 4, 10, 10) — one 10x10 map per head

# Each head produces a different attention pattern
for i in range(4):
    max_attn = weights[0, i].detach().argmax(dim=-1)
    print(f"  Head {i} — each token's peak attention: {max_attn.tolist()}")


# Causal (decoder) mask — token at position i can only attend to positions <= i
def causal_mask(seq_len):
    return torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0)

mask = causal_mask(10)
out_causal, weights_causal = mha(x, x, x, mask=mask)
print("\nWith causal mask — upper triangle should be ~0:")
print(weights_causal[0, 0].detach().round(decimals=2))
