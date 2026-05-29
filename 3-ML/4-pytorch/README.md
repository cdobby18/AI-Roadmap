# 4 · PyTorch

PyTorch is the standard for serious AI work — LLMs, transformers, and most research papers use it. Know the training loop by heart.

---

## What You'll Learn

- Tensors — PyTorch's equivalent to NumPy arrays, but GPU-capable
- `nn.Module` — base class for all neural networks
- The training loop — forward → loss → backward → optimizer.step()
- `torch.no_grad()` — disable gradient tracking during inference

---

## Progress Checklist

- [ ] `01-tensors.py` — create tensors, operations, GPU device handling
- [ ] `02-nn-module.py` — build a custom model with `nn.Module`
- [ ] `03-training-loop.py` — full training loop from scratch

---

## The Training Loop — Memorize This

```python
for epoch in range(epochs):
    predictions = model(X)          # 1. forward pass
    loss = loss_fn(predictions, y)  # 2. compute loss
    optimizer.zero_grad()           # 3. clear old gradients
    loss.backward()                 # 4. compute new gradients
    optimizer.step()                # 5. update weights
```

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `torch.tensor` | Create a tensor from data |
| `nn.Linear(in, out)` | Fully connected layer |
| `nn.ReLU()` | Activation function |
| `nn.BCELoss()` | Binary cross-entropy loss |
| `torch.optim.Adam` | Adaptive optimizer — start here |
| `.backward()` | Compute gradients via autograd |
| `optimizer.zero_grad()` | Must call before each backward, or gradients accumulate |
| `torch.no_grad()` | Disable gradient computation for inference (saves memory) |
| `.to(device)` | Move tensor/model to GPU |

---

## Resources

| Resource | What |
|----------|------|
| PyTorch official tutorials | Learn from the source — tensors through training loops |
| Sentdex — PyTorch playlist | Beginner-friendly, builds incrementally |
