import torch
import math
import matplotlib.pyplot as plt


def positional_encoding(seq_len, d_model):
    # PE[pos, 2i]   = sin(pos / 10000^(2i/d_model))
    # PE[pos, 2i+1] = cos(pos / 10000^(2i/d_model))
    pe = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len).unsqueeze(1).float()
    # Using log-space for numerical stability
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
    )
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe


pe = positional_encoding(seq_len=50, d_model=64)
print("PE shape:", pe.shape)   # (50, 64) — one vector per position

# Visualize — rows = positions, columns = dimensions
# Notice the wave patterns: low-freq waves in high dimensions, high-freq in low
plt.figure(figsize=(12, 5))
plt.imshow(pe.numpy(), aspect="auto", cmap="RdBu")
plt.colorbar()
plt.xlabel("Embedding dimension")
plt.ylabel("Sequence position")
plt.title("Sinusoidal Positional Encoding")
plt.tight_layout()
plt.savefig("positional_encoding.png")
print("Saved positional_encoding.png — open it to see the wave pattern")

# Show that nearby positions have similar encodings
print("\nCosine similarity between positions:")
p0 = pe[0] / pe[0].norm()
p1 = pe[1] / pe[1].norm()
p5 = pe[5] / pe[5].norm()
p49 = pe[49] / pe[49].norm()
print(f"  pos 0 vs pos 1  : {(p0 @ p1).item():.4f}")   # very similar
print(f"  pos 0 vs pos 5  : {(p0 @ p5).item():.4f}")   # less similar
print(f"  pos 0 vs pos 49 : {(p0 @ p49).item():.4f}")  # quite different

# How it's used in practice: added directly to the token embedding before attention
d_model = 64
seq_len = 10
token_embeddings = torch.rand(1, seq_len, d_model)      # shape: (batch, seq, d_model)
pe_slice = positional_encoding(seq_len, d_model)        # shape: (seq, d_model)
x = token_embeddings + pe_slice.unsqueeze(0)            # broadcast over batch
print("\nInput to first attention layer shape:", x.shape)
