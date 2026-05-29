"""
Weights & Biases (W&B) — never train blind again.
Log metrics, compare runs, and visualize results in one dashboard.
Run: pip install wandb && wandb login
"""
import wandb
import torch
import torch.nn as nn

# Initialize a new run
wandb.init(project="ml-roadmap", name="first-training-run")

# Log hyperparameters
config = wandb.config
config.learning_rate = 0.01
config.epochs = 100
config.batch_size = 32

# Toy model and data
X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y = torch.tensor([[0.0], [0.0], [0.0], [1.0], [1.0], [1.0]])

model = nn.Sequential(nn.Linear(1, 4), nn.ReLU(), nn.Linear(4, 1), nn.Sigmoid())
loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)

for epoch in range(config.epochs):
    predictions = model(X)
    loss = loss_fn(predictions, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Log metrics — visible in W&B dashboard
    wandb.log({"epoch": epoch + 1, "loss": loss.item()})

wandb.finish()
print("Run complete — view results at wandb.ai")
