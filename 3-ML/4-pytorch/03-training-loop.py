"""
The PyTorch training loop — memorize this pattern.
Every training run follows: forward → loss → backward → step.
"""
import torch
import torch.nn as nn

# Toy binary classification dataset
X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y = torch.tensor([[0.0], [0.0], [0.0], [1.0], [1.0], [1.0]])

model = nn.Sequential(
    nn.Linear(1, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid(),
)

loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(200):
    # 1. Forward pass
    predictions = model(X)

    # 2. Compute loss
    loss = loss_fn(predictions, y)

    # 3. Zero gradients from previous step
    optimizer.zero_grad()

    # 4. Backward pass (compute gradients)
    loss.backward()

    # 5. Update weights
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch + 1}/200 — Loss: {loss.item():.4f}")

# Inference
with torch.no_grad():
    test = torch.tensor([[3.5]])
    pred = model(test)
    print(f"\nPrediction for 3.5: {pred.item():.4f}")
    print("Class:", (pred > 0.5).int().item())
