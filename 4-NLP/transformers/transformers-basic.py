import torch
import torch.nn as nn


class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, num_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, x):
        attended, _ = self.attention(x, x, x)
        x = self.norm1(x + attended)       # add & norm
        x = self.norm2(x + self.ff(x))    # feed-forward + add & norm
        return x


block = TransformerBlock(d_model=64, num_heads=4, d_ff=256)

x = torch.rand(1, 10, 64)    # batch=1, seq_len=10, d_model=64
output = block(x)

print("Input shape: ", x.shape)
print("Output shape:", output.shape)   # same shape — transformer preserves dimensions
