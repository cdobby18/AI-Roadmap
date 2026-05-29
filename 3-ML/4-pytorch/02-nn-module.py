"""
nn.Module is PyTorch's base class for all neural networks.
Every custom model subclasses it and implements forward().
"""
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 8)   # input_features → hidden
        self.fc2 = nn.Linear(8, 1)   # hidden → output
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x


model = SimpleNet()
print(model)

# Single forward pass with random input
x = torch.rand(4, 2)   # batch of 4, each with 2 features
output = model(x)
print("Output shape:", output.shape)
print("Output:", output)
