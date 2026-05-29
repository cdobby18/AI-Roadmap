"""
PyTorch tensors are the equivalent of NumPy arrays but GPU-capable
and able to track gradients for backpropagation.
"""
import torch

# Creating tensors
t = torch.tensor([1.0, 2.0, 3.0])
zeros = torch.zeros(3, 3)
ones = torch.ones(2, 4)
rand = torch.rand(3, 3)

print(t)
print(zeros)
print(rand)

# Operations
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])
print(a + b)
print(torch.dot(a, b))

# Shape and dimensions
print(t.shape)
print(t.ndim)

# Convert from NumPy
import numpy as np
arr = np.array([1, 2, 3])
t_from_np = torch.from_numpy(arr)
print(t_from_np)

# Move to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
t = t.to(device)
print("Device:", t.device)
