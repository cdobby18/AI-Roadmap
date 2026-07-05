# 3 · Transformers

The architecture behind every modern LLM. These files build attention from scratch first (so the mechanics aren't a black box), then show the same concepts through Hugging Face's pre-built encoder/decoder models.

---

## Progress Checklist

### Attention, from scratch
- [x] `attention-mech.py` — scaled dot-product attention: `softmax(QK^T / sqrt(d_k)) · V`, single head
- [x] `multi-head-attention.py` — full `MultiHeadAttention` module from scratch (separate `W_q`/`W_k`/`W_v`/`W_o` projections, head split/merge) + causal mask demo for decoder-style attention
- [x] `positional-encoding.py` — sinusoidal positional encoding, visualized as a wave pattern, added to token embeddings before the first attention layer

### Assembling a block
- [x] `simple-transform-class.py` — one full encoder `TransformerBlock`: `nn.MultiheadAttention` + residual + `LayerNorm` + feed-forward + residual + `LayerNorm`

### Using pre-trained transformers
- [x] `transformers-basic.py` — encoder (BERT, bidirectional) vs decoder (GPT-2, causal) side by side — hidden states shape vs next-token logits shape
- [x] `bert-embed.py` — BERT embedding extraction, CLS token vs mean pooling, cosine similarity semantic search over One Piece character bios — this *is* the retrieval step of RAG (see `../../8-Projects/phase-4-vivre-card/`)

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| Query, Key, Value | A token's Query is compared against every other token's Key to get attention weights, which combine the Values |
| Scaled dot-product | Divide by `sqrt(d_k)` before softmax — keeps gradients stable as dimension grows |
| Multi-head attention | Several attention "heads" in parallel, each free to specialize (syntax, coreference, etc.), then concatenated and projected back |
| Causal mask | Sets future positions to `-inf` before softmax — used by decoders so token `i` only sees tokens `<= i` |
| Positional encoding | Sinusoidal signal added to embeddings — attention has no built-in sense of order, unlike RNNs |
| Encoder (BERT) | Bidirectional, sees the whole sequence at once — best for classification/understanding/embeddings |
| Decoder (GPT) | Causal, autoregressive — best for generation |
| CLS token vs mean pooling | CLS was designed for fine-tuned classification; mean pooling (average non-padding tokens, masked) is generally better for raw semantic similarity |

---

## Memorize This — Attention in One Function

```python
def scaled_dot_product_attention(Q, K, V):
    d_k = Q.shape[-1]
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights
```

Everything else — multi-head, masking, positional encoding — is scaffolding around this one idea.

---

## Gotcha

`simple-transform-class.py` uses PyTorch's built-in `nn.MultiheadAttention` (not the from-scratch version in `multi-head-attention.py`) — in real code you'd always reach for the built-in; the from-scratch file exists purely so the internals aren't a black box for interviews.
